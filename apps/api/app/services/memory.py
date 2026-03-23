from collections import defaultdict
from typing import Any


class MemoryStore:
    """Minimal in-memory placeholder for session and long-term memory services."""

    def __init__(self) -> None:
        self._session_memory: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._preference_memory: dict[str, dict[str, Any]] = {}

    def remember_event(self, user_id: str, payload: dict[str, Any]) -> None:
        self._session_memory[user_id].append(payload)

    def recent_events(self, user_id: str) -> list[dict[str, Any]]:
        return self._session_memory[user_id][-10:]

    def save_preferences(self, user_id: str, preferences: dict[str, Any]) -> None:
        self._preference_memory[user_id] = preferences

    def get_preferences(self, user_id: str) -> dict[str, Any]:
        return self._preference_memory.get(user_id, {})
