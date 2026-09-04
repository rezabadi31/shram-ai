from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LegibilityStatus(str, Enum):
    EXCELLENT = "EXCELLENT"      # >= 0.90
    ADEQUATE = "ADEQUATE"        # >= 0.75
    DEGRADED = "DEGRADED"        # >= 0.60
    UNREADABLE = "UNREADABLE"    # < 0.60


class RegisterFilingStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    MISSING = "MISSING"
    INCOMPLETE = "INCOMPLETE"


class RegisterComparisonItem(BaseModel):
    register_id: str
    register_name: str
    form_designation: str
    statute: str
    section: str
    mandatory: bool
    status: RegisterFilingStatus
    filing_frequency: str
    penalty_on_default: str
    citation: str
    submitted_document_id: Optional[str] = None
    completeness_score: float = 1.0


class DocumentAgentAuditResult(BaseModel):
    establishment_id: str
    audit_timestamp: str
    overall_legibility_score: float  # 0.0 to 100.0
    legibility_status: LegibilityStatus
    completeness_score: float        # 0.0 to 100.0
    total_required_registers: int
    submitted_count: int
    missing_count: int
    register_comparisons: List[RegisterComparisonItem]
    missing_registers_penalties: List[str]
    agent_recommendation: str
