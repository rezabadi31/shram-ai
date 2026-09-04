from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AgentNodeName(str, Enum):
    SUPERVISOR = "SUPERVISOR"
    DOCUMENT_AGENT = "DOCUMENT_AGENT"
    COMPLIANCE_AGENT = "COMPLIANCE_AGENT"
    RISK_AGENT = "RISK_AGENT"
    EXPLANATION_SYNTHESIS = "EXPLANATION_SYNTHESIS"


class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AgentExecutionStep(BaseModel):
    step_index: int
    node_name: AgentNodeName
    action_taken: str
    timestamp: str
    details: Dict[str, Any] = Field(default_factory=dict)


class OrchestrationExecutionResponse(BaseModel):
    workflow_id: str
    establishment_id: str
    status: WorkflowStatus
    steps_completed: int
    execution_time_ms: float
    compliance_score: float
    risk_score: float
    risk_category: str
    findings_count: int
    steps: List[AgentExecutionStep]
    ai_inspection_brief: Dict[str, Any]
