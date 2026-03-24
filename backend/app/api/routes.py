from fastapi import APIRouter

from app.agents.orchestrator import OrchestratorAgent
from app.core.execution_log import execution_logs
from app.models.schemas import FinalResponse, UserTaskRequest

router = APIRouter(prefix="/v1", tags=["munesh-ai"])
orchestrator = OrchestratorAgent()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "munesh-ai"}


@router.post("/execute", response_model=FinalResponse)
async def execute_task(payload: UserTaskRequest) -> FinalResponse:
    return await orchestrator.run(payload)


@router.get("/logs/{trace_id}")
async def get_logs(trace_id: str) -> dict:
    logs = execution_logs.get(trace_id)
    return {"trace_id": trace_id, "count": len(logs), "logs": [log.model_dump() for log in logs]}
