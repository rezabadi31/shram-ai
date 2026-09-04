from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RuleSeverity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RuleStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"


class StatutoryRuleCategory(str, Enum):
    WAGES = "WAGES"
    HOURS_AND_ATTENDANCE = "HOURS_AND_ATTENDANCE"
    SOCIAL_SECURITY = "SOCIAL_SECURITY"
    SAFETY_AND_HEALTH = "SAFETY_AND_HEALTH"
    REGISTERS_AND_RETURNS = "REGISTERS_AND_RETURNS"


class RuleDefinition(BaseModel):
    rule_id: str
    name: str
    category: StatutoryRuleCategory
    severity: RuleSeverity
    statutory_reference: str
    authority: str
    description: str


class RuleEvaluationFinding(BaseModel):
    rule_id: str
    rule_name: str
    status: RuleStatus
    severity: RuleSeverity
    statutory_reference: str
    authority: str
    evidence: str
    affected_entities_count: int = 0
    affected_entity_ids: List[str] = Field(default_factory=list)


class ComplianceAuditReport(BaseModel):
    establishment_id: str
    audit_timestamp: str
    total_rules_evaluated: int
    passed_count: int
    failed_count: int
    warning_count: int
    overall_compliance_score: float  # 0.0 to 100.0
    findings: List[RuleEvaluationFinding]
