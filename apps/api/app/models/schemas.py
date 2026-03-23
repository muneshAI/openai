from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    RESEARCH = "research"
    DECISION = "decision"
    EXECUTION = "execution"
    CODING = "coding"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETE = "complete"


class CommandRequest(BaseModel):
    user_id: str
    command: str = Field(..., min_length=5)
    locale: str = "en-NP"
    industry: str = "telecom"
    market: str = "Nepal"


class Task(BaseModel):
    id: str
    title: str
    owner: AgentType
    status: TaskStatus = TaskStatus.PENDING
    description: str
    dependencies: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DecisionAnalysis(BaseModel):
    recommendation: str
    pros: list[str]
    cons: list[str]
    roi_estimate: str
    risk_analysis: list[str]


class CommandResponse(BaseModel):
    mission: str
    summary: str
    tasks: list[Task]
    decisions: DecisionAnalysis
    automations: list[str]
    artifacts: list[str]
    next_actions: list[str]
