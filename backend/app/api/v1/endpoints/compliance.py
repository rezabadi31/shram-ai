from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, Body
from app.schemas.compliance import RuleDefinition, ComplianceAuditReport
from app.compliance.rule_engine import ComplianceRuleEngine
from app.compliance.compliance_checker import ComplianceCheckerService

router = APIRouter()


@router.get("/rules", response_model=List[RuleDefinition], tags=["Compliance Rule Engine"])
async def list_compliance_rules():
    """Returns the registered declarative statutory rules under the Four Labour Codes."""
    return ComplianceRuleEngine.load_rules()


@router.post("/evaluate", response_model=ComplianceAuditReport, tags=["Compliance Rule Engine"])
async def evaluate_establishment_compliance(
    establishment_id: str = Query("EST-001", description="Target establishment ID"),
    payload: Optional[Dict[str, Any]] = Body(default=None),
):
    """
    Executes deterministic compliance rules against canonical records.
    Returns structured pass/fail statuses, mathematical evidence, and exact statutory citations.
    """
    wage_records = payload.get("wage_records") if payload else None
    attendance_records = payload.get("attendance_records") if payload else None
    uploaded_categories = payload.get("uploaded_categories") if payload else None
    worker_count = payload.get("worker_count", 420) if payload else 420
    has_safety_record = payload.get("has_safety_record", False) if payload else False

    return ComplianceCheckerService.run_establishment_audit(
        establishment_id=establishment_id,
        wage_records=wage_records,
        attendance_records=attendance_records,
        uploaded_categories=uploaded_categories,
        worker_count=worker_count,
        has_safety_record=has_safety_record,
    )
