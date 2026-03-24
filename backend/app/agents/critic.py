from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.models.schemas import AgentResult, AgentRole, TaskStatus


class CriticAgent(BaseAgent):
    role = AgentRole.CRITIC

    async def validate(self, ctx: AgentContext, results: list[AgentResult]) -> tuple[TaskStatus, list[str]]:
        await self.log(ctx, "Validating executor results", {"result_count": len(results)})
        issues: list[str] = []
        for result in results:
            if result.status != TaskStatus.SUCCESS:
                issues.append(f"Task {result.task_id} failed: {result.error or result.output}")
        return (TaskStatus.SUCCESS if not issues else TaskStatus.RETRY, issues)
