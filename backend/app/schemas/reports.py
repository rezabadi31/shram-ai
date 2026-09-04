"""
Pydantic Schemas for Statutory Reports and Safe Harbour Certification.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CureActionRequest(BaseModel):
    action_ids: List[str] = Field(..., description="IDs of corrective action items that have been cured")
    proof_document_names: Optional[List[str]] = Field(default_factory=list, description="Associated uploaded proof files")
    remarks: Optional[str] = Field(None, description="Employer compliance notes on remediation")


class RecalibrationResponse(BaseModel):
    establishment_id: str
    establishment_name: str
    previous_score: float
    recalibrated_score: float
    score_delta_to_safe_harbour: float
    safe_harbour_eligible: bool
    cured_actions_count: int
    remaining_actions_count: int
    residual_penalty_exposure_inr: float
    penalty_reduction_inr: float
    timestamp: str


class SafeHarbourCertificateSchema(BaseModel):
    certificate_id: str
    certificate_number: str
    establishment_id: str
    establishment_name: str
    lin: str
    registration_number: str
    jurisdiction: str
    certified_compliance_score: float
    safe_harbour_status: str
    issue_date: str
    expiry_date: str
    validity_days: int = 180
    statutory_citations: List[str]
    cured_violations_summary: List[str]
    verification_hash_sha256: str
    issuing_authority: str
    digital_seal_id: str


class InspectorReportDownloadSchema(BaseModel):
    report_id: str
    report_title: str
    establishment_id: str
    establishment_name: str
    lin: str
    industry: str
    jurisdiction: str
    composite_risk_score: float
    risk_classification: str
    percentile_rank: str
    generated_at: str
    executive_summary: str
    top_shap_contributors: List[Dict[str, Any]]
    compliance_findings: List[Dict[str, Any]]
    cross_document_anomalies: List[Dict[str, Any]]
    recommended_inspection_focus: List[str]
    statutory_provisions_applicable: List[str]
    evidence_graph_nodes_count: int
