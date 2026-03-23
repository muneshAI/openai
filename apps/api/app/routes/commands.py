from fastapi import APIRouter, Depends

from app.models.schemas import CommandRequest, CommandResponse
from app.services.decision_engine import DecisionEngine
from app.services.memory import MemoryStore
from app.services.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/commands", tags=["commands"])
memory_store = MemoryStore()
decision_engine = DecisionEngine()


def get_orchestrator() -> AgentOrchestrator:
    return AgentOrchestrator(memory_store=memory_store, decision_engine=decision_engine)


@router.post("/execute", response_model=CommandResponse)
def execute_command(
    payload: CommandRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
) -> CommandResponse:
    return orchestrator.run(payload)
