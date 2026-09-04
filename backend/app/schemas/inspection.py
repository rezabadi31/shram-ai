from typing import List, Optional
from pydantic import BaseModel, Field
import datetime


class InspectionChecklistItem(BaseModel):
    item_id: str
    category: str
    description: str
    statutory_ref: str
    is_verified: bool = False
    finding: Optional[str] = None
    severity: str = "NONE"  # NONE | LOW | MEDIUM | HIGH | CRITICAL


class ViolationDocketEntry(BaseModel):
    violation_id: str
    code_section: str
    description: str
    evidence_collected: List[str]
    suggested_penalty_inr: float
    severity: str


class InspectionSession(BaseModel):
    session_id: str
    establishment_id: str
    establishment_name: str
    inspector_id: str
    started_at: str
    status: str  # ACTIVE | SUBMITTED | CLOSED
    checklist: List[InspectionChecklistItem]
    violations_found: int
    documents_seized: List[str]
    field_notes: str
    violation_docket: List[ViolationDocketEntry]
    total_penalty_proposed_inr: float


class InspectionSessionSubmitRequest(BaseModel):
    session_id: str
    establishment_id: str
    inspector_id: str
    checklist: List[InspectionChecklistItem]
    documents_seized: List[str]
    field_notes: str


class InspectionSessionResponse(BaseModel):
    session_id: str
    status: str
    violations_found: int
    total_penalty_proposed_inr: float
    violation_docket: List[ViolationDocketEntry]
    report_ref: str
    timestamp: str
