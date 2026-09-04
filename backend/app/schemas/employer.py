from typing import List, Optional
from pydantic import BaseModel, Field


class PenaltyExposureItem(BaseModel):
    code_name: str
    section: str
    violation_description: str
    maximum_fine_inr: float
    applicable: bool


class RegisterStatusItem(BaseModel):
    name: str
    status: str
    last_processed: str
    audit_badge: str
    issues_count: int


class CorrectiveActionItem(BaseModel):
    issue: str
    statutory_ref: str
    recommended_action: str
    priority: str
    estimated_arrears_inr: float
    deadline: str


class EmployerComplianceProfile(BaseModel):
    establishment_id: str
    establishment_name: str
    lin: str
    registration_number: str
    jurisdiction: str
    ml_risk_score: float
    priority_class: str
    voluntary_compliance_score: int
    score_delta_to_safe_harbour: int
    total_penalty_exposure_inr: float
    missing_filings_count: int
    flagged_issues_count: int
    register_statuses: List[RegisterStatusItem]
    corrective_actions: List[CorrectiveActionItem]
    penalty_exposures: List[PenaltyExposureItem]
    safe_harbour_window_days: int = 14
    timestamp: str
