from typing import Optional, Dict, Any
from fastapi import APIRouter, Query, Body
from app.schemas.compliance_agent import ComplianceAgentAuditResult
from app.agents.compliance_agent import ComplianceAgentService

router = APIRouter()


@router.post("/audit", response_model=ComplianceAgentAuditResult, tags=["Compliance Agent"])
async def run_compliance_agent_audit(
    establishment_id: str = Query("EST-001", description="Target establishment ID to audit"),
    payload: Optional[Dict[str, Any]] = Body(default=None),
):
    """
    Triggers autonomous Compliance Agent:
    - Runs deterministic statutory rules
    - Queries Labour Law RAG for ground-truth statutory citations
    - Anchors row-level document evidence (page, row, discrepancy)
    - Synthesizes grounded legal rationale and actionable enforcement remedies
    """
    wage_records = payload.get("wage_records") if payload else None
    attendance_records = payload.get("attendance_records") if payload else None
    uploaded_categories = payload.get("uploaded_categories") if payload else None
    worker_count = payload.get("worker_count", 420) if payload else 420

    return ComplianceAgentService.run_compliance_audit(
        establishment_id=establishment_id,
        wage_records=wage_records,
        attendance_records=attendance_records,
        uploaded_categories=uploaded_categories,
        worker_count=worker_count,
    )
