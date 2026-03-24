from __future__ import annotations

from collections import defaultdict

from app.models.schemas import ExecutionLog


class ExecutionLogStore:
    """In-memory execution log store; replace with Redis stream or DB table in production."""

    def __init__(self):
        self._logs: dict[str, list[ExecutionLog]] = defaultdict(list)

    def add(self, log: ExecutionLog) -> None:
        self._logs[log.trace_id].append(log)

    def get(self, trace_id: str) -> list[ExecutionLog]:
        return self._logs.get(trace_id, [])


execution_logs = ExecutionLogStore()
