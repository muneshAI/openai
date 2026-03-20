from __future__ import annotations

import argparse
import hashlib
import json
import logging
import mimetypes
import os
import shutil
import signal
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

try:
    from watchdog.events import FileSystemEvent, FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:  # pragma: no cover - optional until installed
    FileSystemEvent = Any  # type: ignore[assignment]

    class FileSystemEventHandler:  # type: ignore[override]
        pass

    Observer = None

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    Table = None

try:
    from send2trash import send2trash
except ImportError:  # pragma: no cover - optional dependency
    send2trash = None


DEFAULT_CONFIG = {
    "target_directory": "~/Downloads",
    "log_file": "~/file_organizer/file_organizer.log",
    "dry_run": True,
    "use_trash": True,
    "confirm_destructive_actions": True,
    "archive_directory_name": "Archive",
    "organized_directories": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
        "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf", ".md", ".csv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".rb", ".php", ".html", ".css", ".json", ".yaml", ".yml", ".sh"],
        "Others": []
    },
    "cleanup": {
        "delete_empty_folders": True,
        "detect_duplicates": True,
        "large_file_threshold_mb": 100,
        "unused_days": 30,
        "archive_large_unused_files": True
    },
    "protected_paths": [
        "~",
        "~/Desktop",
        "~/Documents",
        "~/Downloads",
        "/",
        "/System",
        "/Library",
        "/Applications",
        "C:/Windows",
        "C:/Program Files",
        "C:/Program Files (x86)"
    ],
    "ai_categorization": {
        "enabled": True,
        "keyword_rules": {
            "Images": ["screenshot", "photo", "image", "wallpaper"],
            "Videos": ["movie", "clip", "screenrecord", "recording"],
            "Documents": ["invoice", "receipt", "report", "resume", "notes"],
            "Audio": ["podcast", "voice", "track", "song"],
            "Archives": ["backup", "archive", "bundle"],
            "Code": ["script", "source", "project", "repo"]
        }
    },
    "notifications": {
        "enabled": False,
        "summary_email": ""
    },
    "schedule": {
        "enabled": False,
        "interval_minutes": 60
    }
}


@dataclass
class ActionRecord:
    timestamp: str
    action: str
    source: str
    destination: str = ""
    status: str = "ok"
    details: str = ""


class UserInterface:
    def __init__(self) -> None:
        self.console = Console() if Console else None

    def info(self, message: str) -> None:
        if self.console:
            self.console.print(f"[cyan]{message}[/cyan]")
        else:
            print(message)

    def success(self, message: str) -> None:
        if self.console:
            self.console.print(f"[green]{message}[/green]")
        else:
            print(message)

    def warning(self, message: str) -> None:
        if self.console:
            self.console.print(f"[yellow]{message}[/yellow]")
        else:
            print(message)

    def error(self, message: str) -> None:
        if self.console:
            self.console.print(f"[red]{message}[/red]")
        else:
            print(message, file=sys.stderr)

    def render_summary(self, processed: int, actions: list[ActionRecord]) -> None:
        if self.console and Table:
            table = Table(title=f"Processed files: {processed}")
            table.add_column("Timestamp")
            table.add_column("Action")
            table.add_column("Source")
            table.add_column("Destination")
            table.add_column("Status")
            for item in actions[-15:]:
                table.add_row(item.timestamp, item.action, item.source, item.destination, item.status)
            self.console.print(table)
            return

        self.info(f"Processed files: {processed}")
        for item in actions[-15:]:
            self.info(f"[{item.timestamp}] {item.action}: {item.source} -> {item.destination or '-'} ({item.status})")


class ConfigManager:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            self.save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()

        with self.path.open("r", encoding="utf-8") as handle:
            user_config = json.load(handle)
        return self._merge(DEFAULT_CONFIG, user_config)

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    def _merge(self, defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
        merged: dict[str, Any] = dict(defaults)
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = self._merge(merged[key], value)
            else:
                merged[key] = value
        return merged


class FileOrganizer:
    def __init__(
        self,
        config: dict[str, Any],
        ui: UserInterface,
        *,
        dry_run: Optional[bool] = None,
        confirm_destructive: Optional[bool] = None,
    ) -> None:
        self.config = config
        self.ui = ui
        self.target_directory = Path(config["target_directory"]).expanduser().resolve()
        self.archive_directory = self.target_directory / config.get("archive_directory_name", "Archive")
        self.log_file = Path(config["log_file"]).expanduser()
        self.dry_run = config["dry_run"] if dry_run is None else dry_run
        self.confirm_destructive = (
            config.get("confirm_destructive_actions", True)
            if confirm_destructive is None
            else confirm_destructive
        )
        self.use_trash = bool(config.get("use_trash", True))
        self.category_map = self._build_extension_lookup(config["organized_directories"])
        self.ai_rules = config.get("ai_categorization", {})
        self.actions: list[ActionRecord] = []
        self.processed_files = 0
        self._logger = self._configure_logging()
        self._protected_paths = self._resolve_protected_paths(config.get("protected_paths", []))
        self._lock = threading.Lock()

    def _configure_logging(self) -> logging.Logger:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("desktop_automation")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.FileHandler(self.log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _resolve_protected_paths(self, raw_paths: Iterable[str]) -> set[Path]:
        resolved = set()
        for item in raw_paths:
            try:
                resolved.add(Path(item).expanduser().resolve())
            except OSError:
                continue
        return resolved

    def _build_extension_lookup(self, mapping: dict[str, list[str]]) -> dict[str, str]:
        lookup: dict[str, str] = {}
        for category, extensions in mapping.items():
            for ext in extensions:
                lookup[ext.lower()] = category
        return lookup

    def _record(self, action: str, source: Path, destination: Optional[Path] = None, *, status: str = "ok", details: str = "") -> None:
        item = ActionRecord(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            action=action,
            source=str(source),
            destination=str(destination) if destination else "",
            status=status,
            details=details,
        )
        self.actions.append(item)
        message = f"{action} | {source}"
        if destination:
            message += f" -> {destination}"
        if details:
            message += f" | {details}"
        if status != "ok":
            self._logger.warning(message)
        else:
            self._logger.info(message)

    def _is_within_target(self, path: Path) -> bool:
        try:
            path.resolve().relative_to(self.target_directory)
            return True
        except ValueError:
            return False

    def _is_safe_path(self, path: Path) -> bool:
        resolved = path.resolve()
        if not self._is_within_target(resolved):
            return False

        system_protected = {
            protected
            for protected in self._protected_paths
            if protected == Path(protected.anchor) or not self.target_directory.is_relative_to(protected)
        }
        return resolved != self.target_directory and not any(resolved == protected for protected in system_protected)

    def _should_skip(self, path: Path) -> bool:
        return (
            not path.exists()
            or path.is_dir()
            or path.name.startswith('.')
            or path == self.log_file
            or self.archive_directory in path.parents
        )

    def categorize_file(self, path: Path) -> str:
        extension = path.suffix.lower()
        if extension in self.category_map:
            return self.category_map[extension]

        if self.ai_rules.get("enabled", False):
            stem = path.stem.lower()
            for category, keywords in self.ai_rules.get("keyword_rules", {}).items():
                if any(keyword in stem for keyword in keywords):
                    return category

        mime_type, _ = mimetypes.guess_type(path.name)
        if mime_type:
            if mime_type.startswith("image/"):
                return "Images"
            if mime_type.startswith("video/"):
                return "Videos"
            if mime_type.startswith("audio/"):
                return "Audio"
            if mime_type in {"application/pdf", "text/plain"} or mime_type.startswith("text/"):
                return "Documents"

        return "Others"

    def normalize_filename(self, path: Path) -> str:
        stat = path.stat()
        date_prefix = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
        sanitized_stem = "_".join(path.stem.strip().split()) or "file"
        return f"{date_prefix}_{sanitized_stem}{path.suffix.lower()}"

    def resolve_collision(self, destination: Path) -> Path:
        if not destination.exists():
            return destination

        counter = 1
        while True:
            candidate = destination.with_name(f"{destination.stem}({counter}){destination.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def move_file(self, source: Path, destination: Path) -> Path:
        if self.dry_run:
            self._record("dry-run-move", source, destination)
            return destination

        destination.parent.mkdir(parents=True, exist_ok=True)
        final_destination = self.resolve_collision(destination)
        shutil.move(str(source), str(final_destination))
        self._record("move", source, final_destination)
        return final_destination

    def process_file(self, path: Path) -> Optional[Path]:
        with self._lock:
            if self._should_skip(path):
                return None

            try:
                if not self._is_safe_path(path):
                    self._record("skip-unsafe", path, status="warning", details="Path failed safety checks")
                    return None

                category = self.categorize_file(path)
                renamed = self.normalize_filename(path)
                destination = self.target_directory / category / renamed
                final_destination = self.move_file(path, destination)
                self.processed_files += 1
                return final_destination
            except Exception as exc:  # pragma: no cover - defensive runtime handling
                self._record("error", path, status="error", details=str(exc))
                self.ui.error(f"Failed to process {path}: {exc}")
                return None

    def hash_file(self, path: Path, block_size: int = 1024 * 1024) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            while chunk := handle.read(block_size):
                digest.update(chunk)
        return digest.hexdigest()

    def _confirm(self, message: str) -> bool:
        if not self.confirm_destructive or self.dry_run:
            return True
        response = input(f"{message} [y/N]: ").strip().lower()
        return response in {"y", "yes"}

    def _trash_or_delete(self, path: Path) -> None:
        if self.dry_run:
            self._record("dry-run-delete", path)
            return

        if self.use_trash and send2trash is not None:
            send2trash(str(path))
            self._record("trash", path)
            return

        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()
        self._record("delete", path)

    def cleanup_duplicates(self) -> None:
        if not self.config.get("cleanup", {}).get("detect_duplicates", True):
            return

        hashes: dict[str, Path] = {}
        for path in self._iter_files(self.target_directory):
            if self._should_skip(path):
                continue
            if self.archive_directory in path.parents:
                continue
            try:
                digest = self.hash_file(path)
            except OSError as exc:
                self._record("hash-error", path, status="warning", details=str(exc))
                continue
            original = hashes.get(digest)
            if original is None:
                hashes[digest] = path
                continue
            if self._confirm(f"Duplicate detected: {path}. Remove duplicate?"):
                self._trash_or_delete(path)
                self._record("duplicate-removed", path, original)

    def cleanup_empty_folders(self) -> None:
        if not self.config.get("cleanup", {}).get("delete_empty_folders", True):
            return

        for folder in sorted(self.target_directory.rglob("*"), reverse=True):
            if not folder.is_dir():
                continue
            if folder in {self.target_directory, self.archive_directory}:
                continue
            try:
                next(folder.iterdir())
            except StopIteration:
                if self._is_safe_path(folder) and self._confirm(f"Delete empty folder {folder}?"):
                    self._trash_or_delete(folder)
            except OSError as exc:
                self._record("folder-scan-error", folder, status="warning", details=str(exc))

    def archive_large_unused_files(self) -> None:
        cleanup = self.config.get("cleanup", {})
        if not cleanup.get("archive_large_unused_files", True):
            return

        threshold_bytes = int(cleanup.get("large_file_threshold_mb", 100)) * 1024 * 1024
        cutoff = datetime.now() - timedelta(days=int(cleanup.get("unused_days", 30)))
        for path in self._iter_files(self.target_directory):
            if self._should_skip(path) or self.archive_directory in path.parents:
                continue
            try:
                stat = path.stat()
            except OSError as exc:
                self._record("stat-error", path, status="warning", details=str(exc))
                continue
            last_accessed = datetime.fromtimestamp(stat.st_atime)
            if stat.st_size >= threshold_bytes and last_accessed <= cutoff:
                destination = self.archive_directory / path.name
                self.move_file(path, destination)
                self._record("archive-large-unused", path, destination, details=f"{stat.st_size} bytes")

    def run_cleanup(self) -> None:
        self.cleanup_duplicates()
        self.archive_large_unused_files()
        self.cleanup_empty_folders()

    def scan_and_organize(self) -> None:
        for path in list(self._iter_files(self.target_directory)):
            self.process_file(path)

    def _iter_files(self, root: Path) -> Iterable[Path]:
        for path in root.rglob("*"):
            if path.is_file():
                yield path

    def summary(self) -> None:
        self.ui.render_summary(self.processed_files, self.actions)


class OrganizerEventHandler(FileSystemEventHandler):
    def __init__(self, organizer: FileOrganizer) -> None:
        self.organizer = organizer

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            time.sleep(0.2)
            self.organizer.process_file(Path(event.src_path))

    def on_moved(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            time.sleep(0.2)
            self.organizer.process_file(Path(event.dest_path))


class Scheduler:
    def __init__(self, organizer: FileOrganizer, interval_minutes: int) -> None:
        self.organizer = organizer
        self.interval_seconds = max(interval_minutes, 1) * 60
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def _run(self) -> None:
        while not self._stop.wait(self.interval_seconds):
            self.organizer.scan_and_organize()
            self.organizer.run_cleanup()


class MonitorService:
    def __init__(self, organizer: FileOrganizer) -> None:
        if Observer is None:
            raise RuntimeError("watchdog is required for monitor mode. Install dependencies with: pip install -r requirements.txt")
        self.organizer = organizer
        self.observer = Observer()

    def run(self) -> None:
        handler = OrganizerEventHandler(self.organizer)
        self.observer.schedule(handler, str(self.organizer.target_directory), recursive=True)
        self.observer.start()
        self.organizer.ui.success(f"Monitoring {self.organizer.target_directory}")

        stop_event = threading.Event()

        def _stop(*_: Any) -> None:
            stop_event.set()

        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        try:
            while not stop_event.is_set():
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join(timeout=5)
            self.organizer.summary()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Production-grade desktop file automation")
    parser.add_argument("--config", default="config.json", help="Path to config JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without changing files")
    parser.add_argument("--force", action="store_true", help="Disable confirmation prompts for cleanup actions")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scan", help="Organize files currently in the target directory")
    subparsers.add_parser("cleanup", help="Run maintenance cleanup tasks")
    subparsers.add_parser("monitor", help="Monitor the target directory in real time")
    subparsers.add_parser("run-once", help="Organize files and then run cleanup")
    subparsers.add_parser("init-config", help="Create a default config.json if it does not exist")
    return parser


def load_organizer(args: argparse.Namespace) -> tuple[FileOrganizer, dict[str, Any]]:
    config_path = Path(args.config)
    manager = ConfigManager(config_path)
    if args.command == "init-config":
        if config_path.exists():
            raise FileExistsError(f"Config already exists: {config_path}")
        manager.save(DEFAULT_CONFIG)
        raise SystemExit(f"Created default config at {config_path}")

    config = manager.load()
    ui = UserInterface()
    organizer = FileOrganizer(
        config,
        ui,
        dry_run=args.dry_run or config.get("dry_run", False),
        confirm_destructive=not args.force,
    )
    return organizer, config


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        organizer, config = load_organizer(args)
    except FileExistsError as exc:
        print(exc, file=sys.stderr)
        return 1
    except SystemExit as exc:
        print(exc)
        return 0

    if not organizer.target_directory.exists():
        organizer.ui.error(f"Target directory does not exist: {organizer.target_directory}")
        return 1

    if args.command == "scan":
        organizer.scan_and_organize()
        organizer.summary()
        return 0

    if args.command == "cleanup":
        organizer.run_cleanup()
        organizer.summary()
        return 0

    if args.command == "run-once":
        organizer.scan_and_organize()
        organizer.run_cleanup()
        organizer.summary()
        return 0

    scheduler = None
    schedule_config = config.get("schedule", {})
    if schedule_config.get("enabled", False):
        scheduler = Scheduler(organizer, int(schedule_config.get("interval_minutes", 60)))
        scheduler.start()

    try:
        MonitorService(organizer).run()
    finally:
        if scheduler:
            scheduler.stop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
