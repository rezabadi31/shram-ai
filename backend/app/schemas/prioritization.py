from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PrioritizedEstablishmentItem(BaseModel):
    establishment_id: str
    name: str
    registration_number: str
    industrial_belt: str
    industry_sector: str
    worker_count: int
    ml_risk_score: float = Field(..., description="Calibrated XGBoost Risk Score (0-100)")
    composite_priority_score: float = Field(..., description="Multi-criteria weighted scheduling score (0-100)")
    priority_class: str  # "HIGH", "MEDIUM", "LOW"
    selection_reason: str  # "RISK_DRIVEN" or "RANDOM_AUDIT_CONTROL"
    recency_months: int
    inspection_status: str  # "PENDING", "SCHEDULED", "IN_PROGRESS", "COMPLETED"
    assigned_inspector_id: Optional[str] = None
    target_audit_window: Optional[str] = None


class PrioritizationFilterParams(BaseModel):
    industrial_belt: Optional[str] = None
    industry_sector: Optional[str] = None
    priority_class: Optional[str] = None
    selection_reason: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=5000)


class PrioritizedQueueResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    items: List[PrioritizedEstablishmentItem]


class InspectionScheduleBatchRequest(BaseModel):
    establishment_ids: List[str]
    inspector_id: str = "INS-OFFICER-42"
    urgency: str = "STANDARD"  # "IMMEDIATE_72H", "STANDARD_14D", "ROUTINE_30D"


class InspectionScheduleResponse(BaseModel):
    scheduled_count: int
    inspector_id: str
    target_window: str
    scheduled_items: List[PrioritizedEstablishmentItem]


class QueueSummaryMetrics(BaseModel):
    total_jurisdiction_establishments: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    random_control_quota_count: int
    monthly_inspector_capacity: int
    capacity_utilization_percent: float
