from typing import TypedDict, List, Dict, Any, Optional


class ShramAuditState(TypedDict):
    workflow_id: str
    establishment_id: str
    status: str
    current_node: str
    documents: List[Dict[str, Any]]
    normalized_records: Dict[str, Any]
    rule_findings: List[Dict[str, Any]]
    compliance_score: float
    risk_features: Dict[str, Any]
    risk_score: float
    risk_category: str
    steps: List[Dict[str, Any]]
    ai_inspection_brief: Dict[str, Any]
    next_node: Optional[str]
    errors: List[str]
