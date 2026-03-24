from __future__ import annotations

from dataclasses import dataclass

from app.core.execution_log import execution_logs
from app.core.logging import get_logger
from app.models.schemas import AgentRole, ExecutionLog


@dataclass
class AgentContext:
    trace_id: str


class BaseAgent:
    role: AgentRole

    async def log(self, ctx: AgentContext, message: str, data: dict | None = None) -> None:
        payload = data or {}
        logger = get_logger(ctx.trace_id)
        logger.info(f"[{self.role}] {message} | data={payload}")
        execution_logs.add(ExecutionLog(trace_id=ctx.trace_id, actor=self.role, message=message, data=payload))
