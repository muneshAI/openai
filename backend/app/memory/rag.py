from __future__ import annotations

from app.memory.vector_memory import VectorMemory


class RAGService:
    def __init__(self, memory: VectorMemory):
        self.memory = memory

    async def augment_context(self, goal: str) -> dict:
        docs = await self.memory.retrieve(goal)
        return {
            "retrieved_count": len(docs),
            "knowledge": docs,
        }
