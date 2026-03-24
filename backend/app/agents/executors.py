from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.models.schemas import AgentResult, AgentRole, TaskNode, TaskStatus
from app.tools.api_tool import APITool
from app.tools.code_tool import CodeTool
from app.tools.file_tool import FileTool
from app.tools.web_tool import WebTool


class CodeExecutorAgent(BaseAgent):
    role = AgentRole.CODE

    def __init__(self):
        self.tool = CodeTool()

    async def execute(self, ctx: AgentContext, node: TaskNode) -> AgentResult:
        await self.log(ctx, "Executing code task", {"task_id": node.id})
        output = await self.tool.run(code="print('Munesh AI code agent healthy')")
        return AgentResult(task_id=node.id, agent=self.role, status=TaskStatus.SUCCESS if output["ok"] else TaskStatus.FAILED, output=output)


class WebExecutorAgent(BaseAgent):
    role = AgentRole.WEB

    def __init__(self):
        self.tool = WebTool()

    async def execute(self, ctx: AgentContext, node: TaskNode) -> AgentResult:
        await self.log(ctx, "Executing web task", {"task_id": node.id})
        output = await self.tool.run(url="https://example.com")
        return AgentResult(task_id=node.id, agent=self.role, status=TaskStatus.SUCCESS if output["ok"] else TaskStatus.FAILED, output=output)


class APIExecutorAgent(BaseAgent):
    role = AgentRole.API

    def __init__(self):
        self.tool = APITool()

    async def execute(self, ctx: AgentContext, node: TaskNode) -> AgentResult:
        await self.log(ctx, "Executing api task", {"task_id": node.id})
        output = await self.tool.run(method="GET", url="https://api.github.com")
        return AgentResult(task_id=node.id, agent=self.role, status=TaskStatus.SUCCESS if output["ok"] else TaskStatus.FAILED, output=output)


class FileExecutorAgent(BaseAgent):
    role = AgentRole.FILE

    def __init__(self):
        self.tool = FileTool()

    async def execute(self, ctx: AgentContext, node: TaskNode) -> AgentResult:
        await self.log(ctx, "Executing file task", {"task_id": node.id})
        output = await self.tool.run(action="write", path="/tmp/munesh_artifact.txt", content="generated")
        return AgentResult(task_id=node.id, agent=self.role, status=TaskStatus.SUCCESS if output["ok"] else TaskStatus.FAILED, output=output)
