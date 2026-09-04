from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class NoticeViolationItem(BaseModel):
    statutory_code: str
    section: str
    finding_description: str
    prescribed_fine_inr: float
    rectification_window_days: int


class StatutoryNotice(BaseModel):
    notice_id: str
    notice_number: str
    notice_type: str  # SHOW_CAUSE | CLARIFICATION | COMPOUNDABLE_OFFENCE | RECTIFICATION_ORDER
    establishment_id: str
    establishment_name: str
    registration_number: str
    issuing_authority: str
    issuing_officer: str
    issue_date: str
    response_deadline: str
    status: str  # DRAFT | ISSUED | RESPONDED | COMPOUNDED | CLOSED
    summary_narrative: str
    violations: List[NoticeViolationItem]
    total_penalty_exposure_inr: float
    compoundable: bool
    digital_signature_hash: str
    formal_legal_text: str
    metadata: Optional[Dict[str, Any]] = None


class GenerateNoticeRequest(BaseModel):
    establishment_id: str
    notice_type: Optional[str] = "SHOW_CAUSE"
    issuing_officer: Optional[str] = "INS-OFFICER-37 (Central Sphere)"
    custom_instructions: Optional[str] = None


class UpdateNoticeStatusRequest(BaseModel):
    status: str
    response_notes: Optional[str] = None
