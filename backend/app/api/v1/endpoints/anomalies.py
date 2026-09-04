from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Query, Body
from app.schemas.anomaly import CrossDocumentAuditResult, AnomalyType
from app.anomaly.cross_reconciler import CrossDocumentAnomalyEngine

router = APIRouter()


@router.post("/reconcile", response_model=CrossDocumentAuditResult, tags=["Cross-Document Anomaly Engine"])
async def reconcile_documents(
    establishment_id: str = Query("EST-001", description="Target establishment ID"),
    payload: Optional[Dict[str, Any]] = Body(default=None),
):
    """
    Executes cross-document mathematical & entity reconciliation across:
    - Form B Wage Register
    - Form D Attendance Muster Roll
    - Bank Disbursement Scrolls (UTR)
    - Factory Security Gate Muster
    """
    wage_records = payload.get("wage_records") if payload else None
    attendance_records = payload.get("attendance_records") if payload else None
    bank_disbursements = payload.get("bank_disbursements") if payload else None
    gate_muster_count = payload.get("gate_muster_count", 445) if payload else 445
    statutory_register_count = payload.get("statutory_register_count", 420) if payload else 420

    return CrossDocumentAnomalyEngine.run_establishment_reconciliation(
        establishment_id=establishment_id,
        wage_records=wage_records,
        attendance_records=attendance_records,
        bank_disbursements=bank_disbursements,
        gate_muster_count=gate_muster_count,
        statutory_register_count=statutory_register_count,
    )


@router.get("/types", tags=["Cross-Document Anomaly Engine"])
async def get_anomaly_types():
    """
    Returns the supported cross-document anomaly detection heuristics.
    """
    return [
        {
            "type": AnomalyType.GHOST_WORKER,
            "title": "Ghost / Phantom Worker Detection",
            "rule": "Wage Register net pay > 0 AND Muster Roll attendance days == 0",
            "statutory_risk": "Severe (Payroll embezzlement, Section 50 Code on Wages)",
        },
        {
            "type": AnomalyType.UNCOMPENSATED_ATTENDANCE,
            "title": "Uncompensated Physical Attendance",
            "rule": "Muster Roll days > 0 AND Wage Register net pay == 0",
            "statutory_risk": "Severe (Unpaid wages, Section 17 Code on Wages)",
        },
        {
            "type": AnomalyType.DISBURSEMENT_MISMATCH,
            "title": "Bank Disbursement Net Skimming",
            "rule": "abs(Form B Net - Bank Disbursed UTR) > ₹5.00",
            "statutory_risk": "High (Unauthorized deduction / diversion, Section 18)",
        },
        {
            "type": AnomalyType.CONTRACTOR_SUPPRESSION,
            "title": "Contractor Workforce Suppression",
            "rule": "Gate Security Muster Headcount > Statutory Register Headcount",
            "statutory_risk": "Critical (Evading statutory welfare & safety thresholds)",
        },
    ]
