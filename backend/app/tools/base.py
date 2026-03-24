from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    name: str

    @abstractmethod
    async def run(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError
