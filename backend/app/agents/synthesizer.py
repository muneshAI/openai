from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.models.schemas import AgentResult, AgentRole, FinalResponse, TaskStatus


class SynthesizerAgent(BaseAgent):
    role = AgentRole.SYNTHESIZER

    async def synthesize(self, ctx: AgentContext, goal: str, results: list[AgentResult], status: TaskStatus, issues: list[str]) -> FinalResponse:
        await self.log(ctx, "Synthesizing final response", {"status": status})
        steps = [
            {
                "task_id": r.task_id,
                "agent": r.agent,
                "status": r.status,
                "output_keys": list(r.output.keys()),
            }
            for r in results
        ]
        summary = "Execution completed successfully." if status == TaskStatus.SUCCESS else f"Execution completed with retry recommendations: {issues}"
        return FinalResponse(trace_id=ctx.trace_id, goal=goal, status=status, steps=steps, summary=summary)
