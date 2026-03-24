from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    PLANNER = "planner"
    CODE = "code_executor"
    WEB = "web_executor"
    API = "api_executor"
    FILE = "file_executor"
    CRITIC = "critic"
    SYNTHESIZER = "synthesizer"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"


class UserTaskRequest(BaseModel):
    goal: str = Field(..., min_length=5)
    context: dict[str, Any] = Field(default_factory=dict)


class TaskNode(BaseModel):
    id: str
    description: str
    assigned_agent: AgentRole
    depends_on: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskGraph(BaseModel):
    goal: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    nodes: list[TaskNode]


class AgentResult(BaseModel):
    task_id: str
    agent: AgentRole
    status: TaskStatus
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class ExecutionLog(BaseModel):
    trace_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    actor: AgentRole
    message: str
    data: dict[str, Any] = Field(default_factory=dict)


class FinalResponse(BaseModel):
    trace_id: str
    goal: str
    status: TaskStatus
    steps: list[dict[str, Any]]
    summary: str
    artifacts: dict[str, Any] = Field(default_factory=dict)
