import uuid
import datetime
from typing import List, Optional
from app.schemas.inspection import (
    InspectionSession,
    InspectionChecklistItem,
    ViolationDocketEntry,
    InspectionSessionSubmitRequest,
    InspectionSessionResponse,
)

# In-memory session registry (stateless demo; would be DB-backed in production)
_SESSIONS: dict = {}


STANDARD_CHECKLIST = [
    {
        "item_id": "WR-01",
        "category": "Wage Registers",
        "description": "Verify Form B Wage Register is maintained for all workers with correct minimum wage entries",
        "statutory_ref": "Code on Wages 2019 — Section 6, Form B",
    },
    {
        "item_id": "WR-02",
        "category": "Wage Registers",
        "description": "Verify overtime wage entries are at 2x regular rate and recorded in OT authorization column",
        "statutory_ref": "Code on Wages 2019 — Section 14",
    },
    {
        "item_id": "ATT-01",
        "category": "Attendance Records",
        "description": "Verify Form D Attendance Muster Roll headcount matches wage register headcount",
        "statutory_ref": "Code on Wages 2019 — Section 50, Form D",
    },
    {
        "item_id": "ATT-02",
        "category": "Attendance Records",
        "description": "Cross-check biometric turnstile logs or gate register against muster roll entries",
        "statutory_ref": "Code on Wages 2019 — Section 50",
    },
    {
        "item_id": "PAY-01",
        "category": "Payment Evidence",
        "description": "Verify bank UTR payment scroll matches wage register disbursement amounts",
        "statutory_ref": "Code on Wages 2019 — Section 6(3)",
    },
    {
        "item_id": "SAF-01",
        "category": "Safety Compliance",
        "description": "Verify Safety Committee is constituted and composition order is displayed on factory board",
        "statutory_ref": "OSHWC Code 2020 — Section 23",
    },
    {
        "item_id": "SAF-02",
        "category": "Safety Compliance",
        "description": "Inspect machinery inspection logbook (pressing shop / hazardous areas) signed by Safety Officer",
        "statutory_ref": "OSHWC Code 2020 — Section 28",
    },
    {
        "item_id": "SOC-01",
        "category": "Social Security",
        "description": "Verify ESIC registration and contribution challan for current quarter",
        "statutory_ref": "Social Security Code 2020 — Section 28",
    },
    {
        "item_id": "SOC-02",
        "category": "Social Security",
        "description": "Verify EPF/EPS contribution statement is filed and deposited within prescribed date",
        "statutory_ref": "Social Security Code 2020 — Section 16",
    },
    {
        "item_id": "EMP-01",
        "category": "Employee Records",
        "description": "Verify Form A Employee Register with all mandatory fields (Name, DOJ, Designation, Aadhaar reference)",
        "statutory_ref": "Code on Wages 2019 — Section 50, Form A",
    },
]

PENALTY_MAP = {
    "CRITICAL": 50000.0,
    "HIGH": 20000.0,
    "MEDIUM": 10000.0,
    "LOW": 5000.0,
    "NONE": 0.0,
}


class InspectionService:

    @classmethod
    def create_session(cls, establishment_id: str, establishment_name: str, inspector_id: str) -> InspectionSession:
        session_id = f"INSP-{uuid.uuid4().hex[:8].upper()}"
        checklist = [
            InspectionChecklistItem(**{**item, "is_verified": False, "finding": None, "severity": "NONE"})
            for item in STANDARD_CHECKLIST
        ]
        session = InspectionSession(
            session_id=session_id,
            establishment_id=establishment_id,
            establishment_name=establishment_name,
            inspector_id=inspector_id,
            started_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="ACTIVE",
            checklist=checklist,
            violations_found=0,
            documents_seized=[],
            field_notes="",
            violation_docket=[],
            total_penalty_proposed_inr=0.0,
        )
        _SESSIONS[session_id] = session
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[InspectionSession]:
        return _SESSIONS.get(session_id)

    @classmethod
    def submit_session(cls, req: InspectionSessionSubmitRequest) -> InspectionSessionResponse:
        violations = [item for item in req.checklist if item.severity not in ("NONE", "LOW") or item.finding]
        docket: List[ViolationDocketEntry] = []

        for v in violations:
            if v.severity in ("MEDIUM", "HIGH", "CRITICAL"):
                docket.append(ViolationDocketEntry(
                    violation_id=f"VIO-{uuid.uuid4().hex[:6].upper()}",
                    code_section=v.statutory_ref,
                    description=v.finding or v.description,
                    evidence_collected=[d for d in req.documents_seized] if req.documents_seized else ["Inspector on-site notes"],
                    suggested_penalty_inr=PENALTY_MAP.get(v.severity, 10000.0),
                    severity=v.severity,
                ))

        total_penalty = sum(d.suggested_penalty_inr for d in docket)
        session_id = req.session_id

        # Update session if tracked
        if session_id in _SESSIONS:
            s = _SESSIONS[session_id]
            s.status = "SUBMITTED"
            s.violations_found = len(docket)
            s.violation_docket = docket
            s.total_penalty_proposed_inr = total_penalty
            s.documents_seized = req.documents_seized
            s.field_notes = req.field_notes

        return InspectionSessionResponse(
            session_id=session_id,
            status="SUBMITTED",
            violations_found=len(docket),
            total_penalty_proposed_inr=total_penalty,
            violation_docket=docket,
            report_ref=f"RPT-{uuid.uuid4().hex[:8].upper()}",
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
