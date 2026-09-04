"""
Establishment Intelligence and Inspection Queue Endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.auth import UserResponse, RoleEnum
from app.api.deps import get_current_user_optional, verify_establishment_ownership
from app.schemas.establishment import (
    EstablishmentSummary,
    EstablishmentIntelligenceDossier,
    DocumentRecordSchema,
    ComplianceFindingSchema,
    CrossDocumentAnomalySchema,
    SHAPContributionSchema,
)

router = APIRouter()

# Canonical dataset representing sample establishments for evaluation
SAMPLE_ESTABLISHMENTS: List[EstablishmentSummary] = [
    EstablishmentSummary(
        id="EST-001",
        name="ABC Industries Ltd.",
        registration_number="DL-2024-EM-9921",
        industry="Heavy Engineering & Manufacturing",
        worker_count=62,
        risk_score=87.0,
        risk_category="HIGH",
        findings_count=7,
        anomalies_count=3,
        priority="HIGH",
        status="Audit Flagged",
    ),
    EstablishmentSummary(
        id="EST-002",
        name="XYZ Textiles & Apparel",
        registration_number="MH-2023-TX-4180",
        industry="Garment & Apparel",
        worker_count=145,
        risk_score=74.0,
        risk_category="HIGH",
        findings_count=4,
        anomalies_count=2,
        priority="HIGH",
        status="Under Review",
    ),
    EstablishmentSummary(
        id="EST-003",
        name="PQR Precision Components",
        registration_number="KA-2023-AU-1052",
        industry="Auto Ancillary",
        worker_count=38,
        risk_score=56.0,
        risk_category="MEDIUM",
        findings_count=2,
        anomalies_count=1,
        priority="MEDIUM",
        status="Clarification Requested",
    ),
    EstablishmentSummary(
        id="EST-004",
        name="Bharat Green Logistics",
        registration_number="TN-2024-LG-7714",
        industry="Warehousing & Logistics",
        worker_count=92,
        risk_score=22.0,
        risk_category="LOW",
        findings_count=0,
        anomalies_count=0,
        priority="LOW",
        status="Fully Compliant",
    ),
]


@router.get("", response_model=List[EstablishmentSummary], tags=["Establishments"])
async def list_establishments(current_user: Optional[UserResponse] = Depends(get_current_user_optional)):
    """List all establishments ranked in the inspection priority queue."""
    if current_user and current_user.role == RoleEnum.EMPLOYER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Restricted — Your account does not have Inspector permissions.",
        )
    return SAMPLE_ESTABLISHMENTS


@router.get("/{establishment_id}", response_model=EstablishmentIntelligenceDossier, tags=["Establishments"])
async def get_establishment_dossier(
    establishment_id: str,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """Retrieve full compliance intelligence dossier for a specific establishment."""
    if current_user:
        verify_establishment_ownership(establishment_id, current_user)

    establishment = next((e for e in SAMPLE_ESTABLISHMENTS if e.id == establishment_id), None)
    if not establishment:
        # Default to first if not matched or error
        if establishment_id == "EST-001" or SAMPLE_ESTABLISHMENTS:
            establishment = SAMPLE_ESTABLISHMENTS[0]
        else:
            raise HTTPException(status_code=404, detail="Establishment not found")

    return EstablishmentIntelligenceDossier(
        establishment=establishment,
        documents=[
            DocumentRecordSchema(
                id="DOC-WAGE-01",
                document_type="Wage Register (Form B)",
                filename="ABC_Wage_Register_Oct2024.pdf",
                upload_date="2024-10-15",
                ocr_confidence=0.94,
                status="Processed",
                pages=14,
                extracted_records=57,
            ),
            DocumentRecordSchema(
                id="DOC-ATTN-01",
                document_type="Attendance Muster Roll (Form D)",
                filename="ABC_MusterRoll_Oct2024.pdf",
                upload_date="2024-10-15",
                ocr_confidence=0.91,
                status="Processed",
                pages=8,
                extracted_records=61,
            ),
            DocumentRecordSchema(
                id="DOC-EMP-01",
                document_type="Employee Register (Form A)",
                filename="ABC_Employee_Register.pdf",
                upload_date="2024-09-01",
                ocr_confidence=0.98,
                status="Processed",
                pages=5,
                extracted_records=62,
            ),
            DocumentRecordSchema(
                id="DOC-PAY-01",
                document_type="Payroll Bank Disbursement Sheet",
                filename="ABC_Bank_Disbursement_Oct2024.xlsx",
                upload_date="2024-10-16",
                ocr_confidence=1.0,
                status="Processed",
                pages=6,
                extracted_records=59,
            ),
        ],
        findings=[
            ComplianceFindingSchema(
                id="FND-001",
                rule_id="WAGE-001",
                rule_name="Mandatory Wage Record Completeness",
                severity="HIGH",
                source_document="ABC_Wage_Register_Oct2024.pdf",
                page=4,
                evidence="Row 34 (Worker: Rajesh K.): Missing basic wage rate and statutory overtime calculation breakdown.",
                statutory_reference="Code on Wages 2019, Section 50(1)",
                authority="Chief Labour Commissioner (Central)",
                status="PENDING_VERIFICATION",
            ),
            ComplianceFindingSchema(
                id="FND-002",
                rule_id="WAGE-002",
                rule_name="Minimum Wage Statutory Floor Compliance",
                severity="HIGH",
                source_document="ABC_Wage_Register_Oct2024.pdf",
                page=7,
                evidence="Rows 51-53 (Unskilled Helpers): Daily wage calculated as Rs 310/day, falling below notified floor of Rs 350/day.",
                statutory_reference="Code on Wages 2019, Section 6",
                authority="Ministry of Labour & Employment",
                status="PENDING_VERIFICATION",
            ),
            ComplianceFindingSchema(
                id="FND-003",
                rule_id="ATTN-001",
                rule_name="Mandatory Muster Roll Maintenance",
                severity="MEDIUM",
                source_document="ABC_MusterRoll_Oct2024.pdf",
                page=2,
                evidence="Shift B overtime records omitted for 5 contract workers.",
                statutory_reference="OSH&WC Code 2020, Section 33",
                authority="Directorate General of Mines Safety & Labour Welfare",
                status="PENDING_VERIFICATION",
            ),
        ],
        anomalies=[
            CrossDocumentAnomalySchema(
                id="ANOM-001",
                anomaly_type="Multi-Register Headcount Inconsistency",
                description="Worker count discrepancies across four statutory submissions.",
                involved_registers=["Employee Register", "Attendance Register", "Wage Register", "Payroll Sheet"],
                severity="HIGH",
                detected_discrepancy="Employee Register = 62 | Attendance = 61 | Payroll = 59 | Wage Register = 57",
                evidence_summary="5 active workers present in attendance muster are missing from Form B wage registers.",
            ),
            CrossDocumentAnomalySchema(
                id="ANOM-002",
                anomaly_type="Disbursement Net Discrepancy",
                description="Discrepancy between bank disbursement records and net wage payable column.",
                involved_registers=["Wage Register", "Payroll Bank Sheet"],
                severity="MEDIUM",
                detected_discrepancy="Form B Net Total: Rs 9,42,100 | Bank Disbursement Total: Rs 8,89,500",
                evidence_summary="Net deficit of Rs 52,600 across contract employee payouts.",
            ),
        ],
        risk_breakdown={
            "ml_model": "XGBoost Classifier v0.1",
            "risk_score": 87.0,
            "risk_probability": 0.87,
            "classification": "HIGH",
            "percentile": "94th percentile",
            "recommended_action": "Priority On-Site Statutory Inspection",
        },
        shap_contributions=[
            SHAPContributionSchema(
                feature_name="missing_wage_records",
                feature_label="Missing Wage Records / Field Deficiencies",
                contribution=18.4,
                direction="positive",
            ),
            SHAPContributionSchema(
                feature_name="cross_doc_headcount_mismatch",
                feature_label="Cross-Document Employee Headcount Mismatch",
                contribution=14.2,
                direction="positive",
            ),
            SHAPContributionSchema(
                feature_name="previous_unresolved_findings",
                feature_label="Historical Unresolved Non-Compliance",
                contribution=12.1,
                direction="positive",
            ),
            SHAPContributionSchema(
                feature_name="missing_safety_log",
                feature_label="Expired / Missing Safety Documentation",
                contribution=9.3,
                direction="positive",
            ),
            SHAPContributionSchema(
                feature_name="high_ocr_confidence",
                feature_label="Digital Document Quality & Legibility",
                contribution=-4.0,
                direction="negative",
            ),
        ],
        ai_inspection_brief={
            "priority": "HIGH",
            "risk_score": 87.0,
            "brief_summary": (
                "ABC Industries Ltd. is classified as HIGH RISK primarily due to severe cross-document "
                "inconsistencies (5 workers present in muster rolls are missing from wage sheets) and minimum wage "
                "deficiencies for unskilled staff under the Code on Wages 2019."
            ),
            "critical_focus_areas": [
                "Verify Form B Wage Register entries against Attendance Muster Roll for Shift B.",
                "Inspect bank credit slips for 5 contract workers omitted from wage register.",
                "Confirm minimum wage compliance rate (Statutory floor: Rs 350/day vs paid: Rs 310/day).",
            ],
            "recommended_statutory_documents": [
                "Form B Wage Register (Physical copy with worker sign-offs)",
                "Daily Attendance Muster Roll (Biometric / Sign-in logs)",
                "Bank Disbursement Scroll (NEFT/RTGS transaction records)",
            ],
        },
    )
