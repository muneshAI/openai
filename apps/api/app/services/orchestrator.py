from uuid import uuid4

from app.models.schemas import AgentType, CommandRequest, CommandResponse, Task
from app.services.decision_engine import DecisionEngine
from app.services.memory import MemoryStore


class AgentOrchestrator:
    def __init__(self, memory_store: MemoryStore, decision_engine: DecisionEngine) -> None:
        self.memory_store = memory_store
        self.decision_engine = decision_engine

    def run(self, payload: CommandRequest) -> CommandResponse:
        mission = f"Execute: {payload.command}"
        tasks = self._build_tasks(payload.command)
        decisions = self.decision_engine.evaluate(mission, tasks)

        self.memory_store.remember_event(
            payload.user_id,
            {
                "command": payload.command,
                "market": payload.market,
                "industry": payload.industry,
                "task_count": len(tasks),
            },
        )

        return CommandResponse(
            mission=mission,
            summary=(
                "Munesh AI converted the request into a coordinated telecom-ready execution plan for Nepal, "
                "including research, decision support, automations, and measurable deliverables."
            ),
            tasks=tasks,
            decisions=decisions,
            automations=[
                "Draft Gmail outreach sequence for enterprise prospects.",
                "Prepare WhatsApp campaign workflow for distributor updates.",
                "Create a shared Drive folder and campaign reporting cadence.",
            ],
            artifacts=[
                "Campaign brief",
                "Executive dashboard specification",
                "Outreach asset pack",
            ],
            next_actions=[
                "Approve target segments and budget envelope.",
                "Connect WhatsApp Business and Gmail accounts.",
                "Launch pilot in Bagmati before nationwide rollout.",
            ],
        )

    def _build_tasks(self, command: str) -> list[Task]:
        normalized = command.lower()
        telecom_context = {
            "market": "Nepal",
            "segments": ["prepaid", "enterprise", "distributors"],
            "currency": "NPR",
        }
        return [
            Task(
                id=str(uuid4()),
                title="Research Nepal telecom market dynamics",
                owner=AgentType.RESEARCH,
                description=(
                    "Analyze provincial demand, audience segments, competitor positioning, and channel assumptions."
                ),
                tools=["web_search", "knowledge_base", "analytics_warehouse"],
                metadata={**telecom_context, "source_command": normalized},
            ),
            Task(
                id=str(uuid4()),
                title="Prioritize launch strategy and budget",
                owner=AgentType.DECISION,
                description="Evaluate timeline, ROI, campaign channels, and operating risks.",
                dependencies=[],
                tools=["roi_model", "risk_matrix", "playbook_selector"],
                metadata={**telecom_context, "goal": "province-based rollout"},
            ),
            Task(
                id=str(uuid4()),
                title="Set up automation workflows",
                owner=AgentType.EXECUTION,
                description="Configure messaging, task scheduling, reporting, and file management automations.",
                dependencies=[],
                tools=["gmail", "whatsapp", "slack", "drive", "calendar"],
                metadata={**telecom_context, "requires_approval": True},
            ),
            Task(
                id=str(uuid4()),
                title="Generate launch dashboard and internal tools",
                owner=AgentType.CODING,
                description="Create campaign dashboard, reporting widgets, and reusable internal apps.",
                dependencies=[],
                tools=["react_generator", "api_scaffolder", "dashboard_templates"],
                metadata={**telecom_context, "artifact_type": "dashboard"},
            ),
        ]
