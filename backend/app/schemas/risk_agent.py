from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TacticalEnforcementDirective(BaseModel):
    directive_id: str
    action_type: str  # "PHYSICAL_SURPRISE_INSPECTION", "BANK_SCROLL_DEMAND", "GATE_TURNSTILE_AUDIT", "DESK_NOTICE"
    urgency: str  # "IMMEDIATE_72H", "STANDARD_14D", "ROUTINE_30D"
    description: str
    statutory_authority: str


class RiskAttributionSynthesis(BaseModel):
    top_escalators: List[str]
    top_mitigators: List[str]
    synthesis_narrative: str


class RiskAgentAuditRequest(BaseModel):
    establishment_id: str = "EST-001"
    worker_count: Optional[int] = None
    contract_worker_ratio: Optional[float] = None
    hazardous_process: Optional[bool] = None
    industry_sector: Optional[str] = None
    wage_violation_count: Optional[int] = None
    ot_violation_count: Optional[int] = None
    deduction_violation_count: Optional[int] = None
    missing_register_count: Optional[int] = None
    ghost_worker_count: Optional[int] = None
    uncompensated_worker_count: Optional[int] = None
    disbursement_mismatch_count: Optional[int] = None


class RiskAgentAuditResult(BaseModel):
    establishment_id: str
    ml_model_used: str = Field(..., description="Machine learning model determining the score")
    calibrated_risk_score: float = Field(..., description="Calibrated risk score (0-100) from XGBoost")
    priority_class: str = Field(..., description="HIGH, MEDIUM, or LOW")
    percentile_context: str
    confidence_score: float
    base_jurisdiction_risk: float
    net_shap_escalation: float
    attribution_synthesis: RiskAttributionSynthesis
    enforcement_directives: List[TacticalEnforcementDirective]
    agent_reasoning: str
    timestamp: str


class RiskThresholdsResponse(BaseModel):
    high_threshold: float = 75.0
    medium_threshold: float = 40.0
    low_threshold: float = 0.0
    model_version: str
    calibration_method: str
