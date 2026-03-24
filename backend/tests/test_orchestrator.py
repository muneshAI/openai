import pytest

from app.agents.orchestrator import OrchestratorAgent
from app.models.schemas import TaskStatus, UserTaskRequest


@pytest.mark.asyncio
async def test_orchestrator_runs_end_to_end():
    orchestrator = OrchestratorAgent()
    response = await orchestrator.run(UserTaskRequest(goal="Build a demo app"))
    assert response.goal == "Build a demo app"
    assert response.status in {TaskStatus.SUCCESS, TaskStatus.RETRY}
    assert len(response.steps) >= 1
