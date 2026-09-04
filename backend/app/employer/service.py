import datetime
from typing import List

from app.schemas.employer import (
    EmployerComplianceProfile,
    PenaltyExposureItem,
    RegisterStatusItem,
    CorrectiveActionItem,
)
from app.ml.model_trainer import MLRiskModelTrainer


ESTABLISHMENT_DATA = {
    "EST-001": {
        "name": "ABC Industries Ltd.",
        "lin": "1928374650",
        "reg_no": "MH-PUN-EST-001",
        "jurisdiction": "Central Sphere — Pune, Maharashtra",
        "worker_count": 420,
        "wage_violations": 3,
        "ghost_workers": 1,
    },
    "EST-002": {
        "name": "Bharat Garments Pvt Ltd",
        "lin": "2837465019",
        "reg_no": "TN-CHE-EST-002",
        "jurisdiction": "State Sphere — Chennai, Tamil Nadu",
        "worker_count": 280,
        "wage_violations": 1,
        "ghost_workers": 0,
    },
    "EST-003": {
        "name": "ChemTech Processing Unit",
        "lin": "3746501928",
        "reg_no": "GJ-SUP-EST-003",
        "jurisdiction": "Central Sphere — Surat, Gujarat",
        "worker_count": 310,
        "wage_violations": 4,
        "ghost_workers": 2,
    },
}


class EmployerService:
    """
    Aggregates backend intelligence for the Employer Dashboard:
    - ML risk score from the champion XGBoost model
    - Generative remediation plan from ExplanationService
    - Register statuses, corrective actions, penalty exposure
    """

    @classmethod
    def get_compliance_profile(cls, establishment_id: str = "EST-001") -> EmployerComplianceProfile:
        data = ESTABLISHMENT_DATA.get(establishment_id, ESTABLISHMENT_DATA["EST-001"])

        pred = MLRiskModelTrainer.predict_risk(
            establishment_id=establishment_id,
            worker_count=data["worker_count"],
            wage_violation_count=data["wage_violations"],
            ghost_worker_count=data["ghost_workers"],
        )

        # Voluntary compliance score is inverse of ML risk
        compliance_score = max(10, round(100 - pred.risk_score + 30))
        compliance_score = min(compliance_score, 98)
        safe_harbour_target = 85
        delta = max(0, safe_harbour_target - compliance_score)

        registers = [
            RegisterStatusItem(
                name="Form B Wage Register (Current Quarter)",
                status="Submitted & Audited",
                last_processed="15 Oct 2024",
                audit_badge="2 Issues Found",
                issues_count=2,
            ),
            RegisterStatusItem(
                name="Attendance Muster Roll (Form D)",
                status="Submitted & Audited",
                last_processed="15 Oct 2024",
                audit_badge="1 Issue Found",
                issues_count=1,
            ),
            RegisterStatusItem(
                name="Employee Register Form A",
                status="Verified Active",
                last_processed="01 Sep 2024",
                audit_badge="Compliant",
                issues_count=0,
            ),
            RegisterStatusItem(
                name="Bank Payout Reconciliation Scroll",
                status="Submitted",
                last_processed="16 Oct 2024",
                audit_badge="Reconciled",
                issues_count=0,
            ),
        ]

        corrective = [
            CorrectiveActionItem(
                issue=f"Daily wage for {data['wage_violations']} workers fell below statutory minimum floor",
                statutory_ref="Code on Wages 2019, Section 6(1)",
                recommended_action="Review Shift B wage entries and disburse statutory wage differential arrears.",
                priority="CRITICAL",
                estimated_arrears_inr=7800.0,
                deadline="Within 7 days",
            ),
            CorrectiveActionItem(
                issue="Headcount gap: 5 workers on muster roll not reflected on wage register",
                statutory_ref="Code on Wages 2019, Section 50",
                recommended_action="Upload updated wage disbursement scroll or contractor invoice matching muster roll workers.",
                priority="HIGH",
                estimated_arrears_inr=3400.0,
                deadline="Within 10 days",
            ),
            CorrectiveActionItem(
                issue="Missing quarterly Safety Committee meeting minutes",
                statutory_ref="OSHWC Code 2020, Section 23",
                recommended_action="Constitute Safety Committee, elect worker representatives, and file constitution notice.",
                priority="MEDIUM",
                estimated_arrears_inr=0.0,
                deadline="Within 14 days",
            ),
        ]

        penalties = cls._compute_penalty_exposure(data["wage_violations"], data["ghost_workers"])
        total_exposure = sum(p.maximum_fine_inr for p in penalties if p.applicable)

        return EmployerComplianceProfile(
            establishment_id=establishment_id,
            establishment_name=data["name"],
            lin=data["lin"],
            registration_number=data["reg_no"],
            jurisdiction=data["jurisdiction"],
            ml_risk_score=pred.risk_score,
            priority_class=pred.priority_class,
            voluntary_compliance_score=compliance_score,
            score_delta_to_safe_harbour=delta,
            total_penalty_exposure_inr=total_exposure,
            missing_filings_count=3,
            flagged_issues_count=5,
            register_statuses=registers,
            corrective_actions=corrective,
            penalty_exposures=penalties,
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    @classmethod
    def _compute_penalty_exposure(cls, wage_violations: int, ghost_workers: int) -> List[PenaltyExposureItem]:
        return [
            PenaltyExposureItem(
                code_name="Code on Wages, 2019",
                section="Section 54(1)",
                violation_description="Payment of wages below statutory minimum floor rate",
                maximum_fine_inr=50000.0,
                applicable=wage_violations > 0,
            ),
            PenaltyExposureItem(
                code_name="Code on Wages, 2019",
                section="Section 54(2)",
                violation_description="Failure to maintain statutory wage registers in prescribed form",
                maximum_fine_inr=20000.0,
                applicable=wage_violations > 0,
            ),
            PenaltyExposureItem(
                code_name="Occupational Safety, Health & Working Conditions Code, 2020",
                section="Section 96",
                violation_description="Non-constitution of mandatory Safety Committee for 250+ worker facility",
                maximum_fine_inr=200000.0,
                applicable=True,
            ),
            PenaltyExposureItem(
                code_name="Code on Wages, 2019",
                section="Section 18",
                violation_description="Ghost worker payroll discrepancy — wage credit without attendance record",
                maximum_fine_inr=50000.0,
                applicable=ghost_workers > 0,
            ),
        ]
