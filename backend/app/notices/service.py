import hashlib
import datetime
import uuid
from typing import List, Optional, Dict
from app.schemas.notice import StatutoryNotice, NoticeViolationItem, GenerateNoticeRequest


# In-memory store for statutory notices
NOTICES_STORE: Dict[str, StatutoryNotice] = {}


def _compute_signature_hash(notice_id: str, establishment_id: str, date_str: str) -> str:
    seed = f"{notice_id}:{establishment_id}:{date_str}:SHRAM-STATUTORY-SEAL-2024"
    return "SHA256:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:32]


def _build_formal_legal_text(
    notice_number: str,
    establishment_name: str,
    registration_no: str,
    officer: str,
    issue_date: str,
    deadline: str,
    violations: List[NoticeViolationItem],
    total_penalty: float,
    compoundable: bool,
) -> str:
    violation_rows = ""
    for idx, v in enumerate(violations, 1):
        violation_rows += (
            f"{idx}. Statutory Authority: {v.statutory_code}, {v.section}\n"
            f"   Grievance / Finding: {v.finding_description}\n"
            f"   Maximum Statutory Fine Exposure: INR {v.prescribed_fine_inr:,.2f}\n"
            f"   Cure Period: {v.rectification_window_days} Days from notice service\n\n"
        )

    compounding_clause = (
        "AND WHEREAS, the offenses enumerated under Serial No. 1 and 2 are compoundable under Section 56 of the Code on Wages, 2019 "
        "prior to the filing of a formal complaint before the Competent Authority;\n\n"
        if compoundable
        else ""
    )

    return f"""================================================================================
                    GOVERNMENT OF INDIA
             MINISTRY OF LABOUR AND EMPLOYMENT
       OFFICE OF THE DEPUTY CHIEF LABOUR COMMISSIONER (CENTRAL)
================================================================================

NOTICE REFERENCE NO: {notice_number}
DATE OF ISSUANCE: {issue_date}

TO:
The Occupier / Principal Employer
{establishment_name}
Registration No. (LIN / Shram Suvidha): {registration_no}

SUBJECT: STATUTORY SHOW CAUSE NOTICE UNDER CODE ON WAGES, 2019 (SECTION 50 & 54)
         AND OSHWC CODE, 2020 (SECTION 96)

WHEREAS, an automated statutory inspection and cross-document reconciliation was
conducted by the ShramAI Digital Compliance Engine under the supervision of
Labour Enforcement Officer {officer};

AND WHEREAS, examination of statutory records and registers revealed the following
prima facie non-compliances and contraventions of labour legislation:

{violation_rows}
{compounding_clause}NOW, THEREFORE, NOTICE IS HEREBY GIVEN requiring you to SHOW CAUSE within 14 days
of the receipt of this notice (on or before {deadline}) as to why statutory penal
proceedings should not be instituted against you under Section 54 of the Code on Wages,
2019 and/or Section 96 of the OSHWC Code, 2020.

You are further directed to submit proof of wage differential arrears disbursement
and rectified Form B / Form D registers via the Shram Suvidha portal, or submit
an application for compounding of offences under Section 56 of the Code on Wages.

TAKE NOTICE that failure to submit an adequate explanation or cure the violations
within the stipulated deadline shall result in the initiation of formal prosecution
before the Chief Judicial Magistrate without further notice.

GIVEN under my hand and digital verification seal.

Issuing Officer: {officer}
Designation: Labour Enforcement Officer (Central)
Digital Seal: {_compute_signature_hash(notice_number, establishment_name, issue_date)}
================================================================================"""


# Seed realistic default notices
def _init_default_notices():
    notice_1_id = "NOT-2024-001"
    v1 = [
        NoticeViolationItem(
            statutory_code="Code on Wages, 2019",
            section="Section 54(1) read with Section 6(1)",
            finding_description="Payment of wages below prescribed statutory minimum floor rate for 3 workers in Shift B.",
            prescribed_fine_inr=50000.0,
            rectification_window_days=7,
        ),
        NoticeViolationItem(
            statutory_code="Code on Wages, 2019",
            section="Section 50 read with Rule 19",
            finding_description="Failure to reconcile Form D Attendance Muster Roll with Form B Wage Register (5 unaccounted workers).",
            prescribed_fine_inr=20000.0,
            rectification_window_days=10,
        ),
        NoticeViolationItem(
            statutory_code="OSHWC Code, 2020",
            section="Section 96 read with Section 23",
            finding_description="Non-constitution of mandatory Joint Safety Committee for manufacturing facility exceeding 250 workers.",
            prescribed_fine_inr=200000.0,
            rectification_window_days=14,
        ),
    ]

    issue_date = "2024-07-05"
    deadline = "2024-07-19"
    NOTICES_STORE[notice_1_id] = StatutoryNotice(
        notice_id=notice_1_id,
        notice_number="CLC/PUNE/2024/SCN-00194",
        notice_type="SHOW_CAUSE",
        establishment_id="EST-001",
        establishment_name="ABC Manufacturing Pvt Ltd",
        registration_number="LIN-MH-PUN-091244",
        issuing_authority="Office of the Deputy Chief Labour Commissioner (Central), Pune",
        issuing_officer="INS-OFFICER-37 (Central Sphere)",
        issue_date=issue_date,
        response_deadline=deadline,
        status="ISSUED",
        summary_narrative="Show cause notice issued regarding minimum wage underpayment, headcount discrepancy across muster rolls, and absence of statutory safety committee.",
        violations=v1,
        total_penalty_exposure_inr=270000.0,
        compoundable=True,
        digital_signature_hash=_compute_signature_hash(notice_1_id, "EST-001", issue_date),
        formal_legal_text=_build_formal_legal_text(
            "CLC/PUNE/2024/SCN-00194",
            "ABC Manufacturing Pvt Ltd",
            "LIN-MH-PUN-091244",
            "INS-OFFICER-37 (Central Sphere)",
            issue_date,
            deadline,
            v1,
            270000.0,
            True,
        ),
        metadata={"delivery_mode": "DIGITAL_SHRAM_SUVIDHA", "dispatch_timestamp": "2024-07-05T14:30:00"},
    )


_init_default_notices()


class NoticeService:
    @staticmethod
    def list_establishment_notices(establishment_id: str) -> List[StatutoryNotice]:
        return [n for n in NOTICES_STORE.values() if n.establishment_id == establishment_id]

    @staticmethod
    def get_notice(notice_id: str) -> Optional[StatutoryNotice]:
        return NOTICES_STORE.get(notice_id)

    @staticmethod
    def generate_notice(req: GenerateNoticeRequest) -> StatutoryNotice:
        notice_id = f"NOT-{datetime.datetime.now().strftime('%Y')}-{uuid.uuid4().hex[:6].upper()}"
        today = datetime.date.today()
        deadline = today + datetime.timedelta(days=14)
        issue_date_str = today.strftime("%Y-%m-%d")
        deadline_str = deadline.strftime("%Y-%m-%d")

        # Establish defaults based on establishment
        est_name = "ABC Manufacturing Pvt Ltd" if req.establishment_id == "EST-001" else f"Establishment {req.establishment_id}"
        reg_no = "LIN-MH-PUN-091244" if req.establishment_id == "EST-001" else f"LIN-{req.establishment_id}"

        violations = [
            NoticeViolationItem(
                statutory_code="Code on Wages, 2019",
                section="Section 54(1) read with Section 6(1)",
                finding_description="Payment of wages below statutory floor rate detected during register audit.",
                prescribed_fine_inr=50000.0,
                rectification_window_days=7,
            ),
            NoticeViolationItem(
                statutory_code="Code on Wages, 2019",
                section="Section 50",
                finding_description="Muster roll and wage scroll attendance discrepancy.",
                prescribed_fine_inr=20000.0,
                rectification_window_days=10,
            ),
            NoticeViolationItem(
                statutory_code="OSHWC Code, 2020",
                section="Section 96",
                finding_description="Non-constitution of mandatory Safety Committee.",
                prescribed_fine_inr=200000.0,
                rectification_window_days=14,
            ),
        ]

        notice_number = f"CLC/CENTRAL/{today.year}/SCN-{uuid.uuid4().hex[:5].upper()}"
        officer = req.issuing_officer or "INS-OFFICER-37 (Central Sphere)"

        legal_text = _build_formal_legal_text(
            notice_number=notice_number,
            establishment_name=est_name,
            registration_no=reg_no,
            officer=officer,
            issue_date=issue_date_str,
            deadline=deadline_str,
            violations=violations,
            total_penalty=270000.0,
            compoundable=True,
        )

        notice = StatutoryNotice(
            notice_id=notice_id,
            notice_number=notice_number,
            notice_type=req.notice_type or "SHOW_CAUSE",
            establishment_id=req.establishment_id,
            establishment_name=est_name,
            registration_number=reg_no,
            issuing_authority="Office of the Deputy Chief Labour Commissioner (Central)",
            issuing_officer=officer,
            issue_date=issue_date_str,
            response_deadline=deadline_str,
            status="ISSUED",
            summary_narrative=f"Formal statutory notice generated under Code on Wages (Section 50/54) and OSHWC Code (Section 96). Rectification window: 14 days.",
            violations=violations,
            total_penalty_exposure_inr=270000.0,
            compoundable=True,
            digital_signature_hash=_compute_signature_hash(notice_id, req.establishment_id, issue_date_str),
            formal_legal_text=legal_text,
            metadata={
                "generated_by": "ShramAI Statutory Notice Engine",
                "custom_instructions": req.custom_instructions,
            },
        )

        NOTICES_STORE[notice_id] = notice
        return notice

    @staticmethod
    def update_notice_status(notice_id: str, status: str, notes: Optional[str] = None) -> Optional[StatutoryNotice]:
        notice = NOTICES_STORE.get(notice_id)
        if not notice:
            return None
        notice.status = status
        if notes and notice.metadata is not None:
            notice.metadata["response_notes"] = notes
        return notice
