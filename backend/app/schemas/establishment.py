"""
Pydantic schemas for Establishment Intelligence, Compliance Findings, and Risk Profiles.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EstablishmentSummary(BaseModel):
    id: str = Field(..., examples=["EST-001"])
    name: str = Field(..., examples=["ABC Industries Ltd."])
    registration_number: str = Field(..., examples=["DL-2024-EM-9921"])
    industry: str = Field(..., examples=["Manufacturing & Textiles"])
    worker_count: int = Field(..., examples=[62])
    risk_score: float = Field(..., examples=[87.0])
    risk_category: str = Field(..., examples=["HIGH"])
    findings_count: int = Field(..., examples=[7])
    anomalies_count: int = Field(..., examples=[3])
    priority: str = Field(..., examples=["HIGH"])
    status: str = Field(default="Audit Pending", examples=["Audit Pending"])


class DocumentRecordSchema(BaseModel):
    id: str
    document_type: str
    filename: str
    upload_date: str
    ocr_confidence: float
    status: str
    pages: int
    extracted_records: int


class ComplianceFindingSchema(BaseModel):
    id: str
    rule_id: str
    rule_name: str
    severity: str  # HIGH, MEDIUM, LOW
    source_document: str
    page: int
    evidence: str
    statutory_reference: str
    authority: str
    status: str  # PENDING_VERIFICATION, CONFIRMED, REJECTED


class CrossDocumentAnomalySchema(BaseModel):
    id: str
    anomaly_type: str
    description: str
    involved_registers: List[str]
    severity: str
    detected_discrepancy: str
    evidence_summary: str


class SHAPContributionSchema(BaseModel):
    feature_name: str
    feature_label: str
    contribution: float
    direction: str  # positive (increases risk) or negative (decreases risk)


class EstablishmentIntelligenceDossier(BaseModel):
    establishment: EstablishmentSummary
    documents: List[DocumentRecordSchema]
    findings: List[ComplianceFindingSchema]
    anomalies: List[CrossDocumentAnomalySchema]
    risk_breakdown: Dict[str, Any]
    shap_contributions: List[SHAPContributionSchema]
    ai_inspection_brief: Dict[str, Any]
