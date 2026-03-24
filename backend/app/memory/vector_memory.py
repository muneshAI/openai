from __future__ import annotations

from typing import Any


class VectorMemory:
    """
    pgvector-backed long-term memory placeholder.

    In production, connect to PostgreSQL and store embeddings in a vector column.
    """

    def __init__(self):
        self._store: list[dict[str, Any]] = []

    async def add_document(self, trace_id: str, text: str, metadata: dict[str, Any]) -> None:
        self._store.append({"trace_id": trace_id, "text": text, "metadata": metadata})

    async def retrieve(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        # Demo retrieval. Replace with ANN search using pgvector cosine distance.
        return [doc for doc in self._store if query.lower() in doc["text"].lower()][:limit]
