from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StatutoryExposureItem(BaseModel):
    code_name: str
    section: str
    contravention: str
    penalty_provision: str


class RemediationStepItem(BaseModel):
    step_number: int
    action: str
    deadline: str
    statutory_cure: str
    estimated_financial_arrears: str


class InspectorExplanationBrief(BaseModel):
    establishment_id: str
    risk_score: float
    priority_class: str
    executive_summary: str
    statutory_exposures: List[StatutoryExposureItem]
    mandatory_documents_to_seize: List[str]
    cross_examination_checklist: List[str]
    investigation_focus_areas: List[str]


class EmployerRemediationPlan(BaseModel):
    establishment_id: str
    advisory_summary: str
    root_cause_analysis: List[str]
    remediation_steps: List[RemediationStepItem]
    safe_harbour_guidelines: str
    total_estimated_arrears_inr: float


class ComprehensiveExplanationResponse(BaseModel):
    establishment_id: str
    establishment_name: str
    ml_risk_score: float
    priority_class: str
    inspector_brief: InspectorExplanationBrief
    employer_remediation: EmployerRemediationPlan
    zero_hallucination_verified: bool
    timestamp: str


class ExplanationGenerationRequest(BaseModel):
    establishment_id: str = "EST-001"
    worker_count: Optional[int] = None
    wage_violation_count: Optional[int] = None
    ghost_worker_count: Optional[int] = None
