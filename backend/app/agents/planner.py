from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.models.schemas import AgentRole, TaskGraph, TaskNode


class PlannerAgent(BaseAgent):
    role = AgentRole.PLANNER

    async def plan(self, ctx: AgentContext, goal: str, rag_context: dict) -> TaskGraph:
        await self.log(ctx, "Planning goal", {"goal": goal, "rag_docs": rag_context.get("retrieved_count", 0)})
        nodes = [
            TaskNode(id="t1", description="Analyze objective and define deliverables", assigned_agent=AgentRole.CODE),
            TaskNode(id="t2", description="Gather reference data from web", assigned_agent=AgentRole.WEB),
            TaskNode(id="t3", description="Call required external APIs", assigned_agent=AgentRole.API),
            TaskNode(id="t4", description="Create and manage project files", assigned_agent=AgentRole.FILE),
            TaskNode(
                id="t5",
                description="Validate all executor outputs",
                assigned_agent=AgentRole.CRITIC,
                depends_on=["t1", "t2", "t3", "t4"],
            ),
        ]
        return TaskGraph(goal=goal, nodes=nodes)
