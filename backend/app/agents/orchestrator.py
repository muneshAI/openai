from __future__ import annotations

import asyncio
import uuid

from app.agents.base import AgentContext
from app.agents.critic import CriticAgent
from app.agents.executors import APIExecutorAgent, CodeExecutorAgent, FileExecutorAgent, WebExecutorAgent
from app.agents.planner import PlannerAgent
from app.agents.synthesizer import SynthesizerAgent
from app.memory.rag import RAGService
from app.memory.session_memory import SessionMemory
from app.memory.vector_memory import VectorMemory
from app.models.schemas import AgentResult, FinalResponse, TaskStatus, UserTaskRequest


class OrchestratorAgent:
    def __init__(self):
        self.session_memory = SessionMemory()
        self.vector_memory = VectorMemory()
        self.rag = RAGService(self.vector_memory)
        self.planner = PlannerAgent()
        self.code_agent = CodeExecutorAgent()
        self.web_agent = WebExecutorAgent()
        self.api_agent = APIExecutorAgent()
        self.file_agent = FileExecutorAgent()
        self.critic = CriticAgent()
        self.synthesizer = SynthesizerAgent()
        self.max_retries = 2

    async def _run_parallel_executors(self, ctx: AgentContext, graph) -> list[AgentResult]:
        tasks = []
        for node in graph.nodes:
            if node.depends_on:
                continue
            if node.assigned_agent.value == "code_executor":
                tasks.append(self.code_agent.execute(ctx, node))
            elif node.assigned_agent.value == "web_executor":
                tasks.append(self.web_agent.execute(ctx, node))
            elif node.assigned_agent.value == "api_executor":
                tasks.append(self.api_agent.execute(ctx, node))
            elif node.assigned_agent.value == "file_executor":
                tasks.append(self.file_agent.execute(ctx, node))
        return await asyncio.gather(*tasks)

    async def run(self, request: UserTaskRequest) -> FinalResponse:
        trace_id = str(uuid.uuid4())
        ctx = AgentContext(trace_id=trace_id)

        self.session_memory.add({"event": "goal_received", "goal": request.goal})
        rag_context = await self.rag.augment_context(request.goal)
        graph = await self.planner.plan(ctx, request.goal, rag_context)

        results: list[AgentResult] = []
        status = TaskStatus.RETRY
        issues: list[str] = ["Not evaluated yet"]

        for attempt in range(self.max_retries + 1):
            executor_results = await self._run_parallel_executors(ctx, graph)
            results = executor_results
            status, issues = await self.critic.validate(ctx, executor_results)

            if status == TaskStatus.SUCCESS:
                break

            if attempt < self.max_retries:
                self.session_memory.add({"event": "retry", "attempt": attempt + 1, "issues": issues})

        final = await self.synthesizer.synthesize(ctx, request.goal, results, status, issues)
        await self.vector_memory.add_document(trace_id, request.goal, {"status": final.status})
        return final
