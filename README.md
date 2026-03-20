# Desktop File Automation

A production-grade Python desktop automation utility that monitors a user-selected folder, organizes files into category folders, performs safe cleanup actions, and keeps a detailed audit log.

## Features

- Real-time monitoring of a target directory using `watchdog`
- Automatic sorting into `Images`, `Videos`, `Documents`, `Audio`, `Archives`, `Code`, and `Others`
- Intelligent renaming using the pattern `YYYY-MM-DD_originalname.ext`
- Collision-safe duplicate naming with suffixes such as `(1)` and `(2)`
- Cleanup tools for:
  - duplicate detection using SHA-256 hashes
  - empty-folder removal
  - archival of large unused files to an `Archive` folder
  - optional trash support through `send2trash`
- Config-driven behavior through `config.json`
- Cross-platform support for Windows, macOS, and Linux
- Safe defaults with dry-run mode enabled and confirmation prompts for destructive actions
- Optional keyword-based categorization and scheduled maintenance mode
- Rich CLI summaries when `rich` is installed

## Project Files

- `main.py` - application entrypoint and automation logic
- `config.json` - configurable paths, rules, and thresholds
- `requirements.txt` - Python dependencies
- `README.md` - setup and usage documentation

## Installation

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize a default configuration if you want to start from scratch:

   ```bash
   python main.py init-config
   ```

## Configuration

Edit `config.json` to fit your machine and workflow.

### Important configuration keys

- `target_directory`: Folder to monitor or scan
- `log_file`: Path to the action log
- `dry_run`: Preview mode; recommended for first use
- `use_trash`: Move deleted items to the system trash when possible
- `confirm_destructive_actions`: Ask before deleting duplicates or empty folders
- `archive_directory_name`: Folder name used for large unused files
- `organized_directories`: Extension-to-category mapping
- `cleanup.large_file_threshold_mb`: Size threshold for old large-file archival
- `cleanup.unused_days`: Access-age threshold for archival
- `schedule.enabled`: Enable periodic background scan-and-clean runs

## Usage

### Dry run organization pass

```bash
python main.py --dry-run scan
```

### Full organization pass without prompts

```bash
python main.py --force run-once
```

### Cleanup only

```bash
python main.py cleanup
```

### Real-time monitoring

```bash
python main.py monitor
```

## How It Works

1. The organizer scans or monitors the configured target directory.
2. Each file is categorized by extension, MIME type, and optional keyword rules.
3. Files are renamed with a date prefix based on their modification timestamp.
4. Files are moved into category folders inside the target directory.
5. Cleanup routines can hash files to detect duplicates, archive old large files, and remove empty folders.
6. All actions are recorded in the configured log file.

## Safety Notes

- Dry-run mode is enabled by default in `config.json`.
- Cleanup actions can prompt for confirmation unless `--force` is used.
- Safety checks prevent processing files outside the configured target directory.
- The script skips hidden files, the log file, and anything already stored under the archive folder.
- Review your `protected_paths` and `target_directory` before disabling dry-run mode.

## Scheduled Maintenance

Set the following in `config.json` to run periodic scan-and-clean cycles while monitoring:

```json
"schedule": {
  "enabled": true,
  "interval_minutes": 60
}
```

## Bonus Ideas Included

- Keyword-based “AI-style” categorization using filenames
- Optional scheduled cleanup mode
- Notification configuration placeholders for future email integrations

## Suggested Production Hardening

- Run the monitor process as a background service (`systemd`, launchd, or Task Scheduler)
- Add unit tests around categorization and path-safety logic
- Integrate desktop or email notifications if summaries are required
- Tailor `protected_paths` to your organization’s compliance and retention needs
