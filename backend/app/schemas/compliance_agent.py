from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EvidenceAnchor(BaseModel):
    document_id: str
    document_name: str
    page_number: int
    row_index: Optional[int] = None
    employee_id: Optional[str] = None
    discrepancy_value: str
    statutory_requirement: str


class StatutoryEnrichment(BaseModel):
    code_id: str
    act_title: str
    section_number: str
    section_title: str
    statutory_quote: str
    authority: str
    penalty_schedule: Optional[str] = None
    relevance_score: float = 0.98


class GroundedComplianceFinding(BaseModel):
    finding_id: str
    rule_id: str
    rule_name: str
    status: str       # FAILED, PASSED, WARNING
    severity: str     # HIGH, MEDIUM, LOW
    explanation: str
    evidence_anchor: EvidenceAnchor
    statutory_enrichment: StatutoryEnrichment
    actionable_remedy: str


class ComplianceAgentAuditResult(BaseModel):
    establishment_id: str
    audit_timestamp: str
    compliance_score: float
    total_rules_evaluated: int
    violations_count: int
    passed_count: int
    findings: List[GroundedComplianceFinding]
    agent_summary: str
