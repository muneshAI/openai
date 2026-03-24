from collections import deque
from typing import Any


class SessionMemory:
    """Short-term conversational memory for active trace."""

    def __init__(self, max_items: int = 100):
        self._events: deque[dict[str, Any]] = deque(maxlen=max_items)

    def add(self, item: dict[str, Any]) -> None:
        self._events.append(item)

    def all(self) -> list[dict[str, Any]]:
        return list(self._events)
