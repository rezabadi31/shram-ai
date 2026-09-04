import uuid
from typing import List
from app.schemas.timeline import TimelineEvent, EstablishmentTimeline

# Per-establishment synthetic audit trails grounded in realistic statutory events
TIMELINE_DATA = {
    "EST-001": [
        {
            "event_type": "DOCUMENT_SUBMITTED",
            "timestamp": "2024-07-02T09:15:00",
            "date_label": "2 Jul 2024",
            "actor": "ABC Industries HR Portal",
            "actor_type": "EMPLOYER",
            "title": "Q1 Statutory Register Batch Submission",
            "description": "Employer submitted Form B Wage Register, Form D Attendance Muster Roll, Form A Employee Register, and Bank UTR Scroll for Q1 2024 via Shram Suvidha portal.",
            "severity": "INFO",
            "metadata": {"documents": ["Form B", "Form D", "Form A", "Bank UTR Scroll"], "quarter": "Q1-2024"},
        },
        {
            "event_type": "COMPLIANCE_EVALUATED",
            "timestamp": "2024-07-02T10:32:00",
            "date_label": "2 Jul 2024",
            "actor": "ShramAI Document Agent",
            "actor_type": "SYSTEM",
            "title": "Automated Rule Engine Evaluation Completed",
            "description": "Deterministic rule engine processed 4 statutory documents. Identified 1 wage rate discrepancy in Form B for Shift B workers and 1 headcount gap between Form D and Form B.",
            "severity": "HIGH",
            "metadata": {"rules_checked": 18, "violations": 2, "compliant": 16},
        },
        {
            "event_type": "ANOMALY_DETECTED",
            "timestamp": "2024-07-02T10:33:45",
            "date_label": "2 Jul 2024",
            "actor": "ShramAI Cross-Register Anomaly Engine",
            "actor_type": "ML_ENGINE",
            "title": "Cross-Register Headcount Anomaly Flagged",
            "description": "5 workers present in Form D Attendance Muster Roll not reflected in Form B Wage Register. Possible ghost worker payroll or unregistered contractor arrangement.",
            "severity": "HIGH",
            "metadata": {"anomaly_type": "HEADCOUNT_MISMATCH", "delta": 5},
        },
        {
            "event_type": "RISK_ASSESSED",
            "timestamp": "2024-07-02T10:35:00",
            "date_label": "2 Jul 2024",
            "actor": "XGBoost ML Risk Model v2.1",
            "actor_type": "ML_ENGINE",
            "title": "ML Risk Score Computed: 84.5 / 100",
            "description": "XGBoost champion model (AUC 0.91, PR-AUC 0.87) computed risk score of 84.5. Key SHAP drivers: wage_violation_count (+28.4), ghost_worker_count (+18.7), high_hazard_sector (+12.3). Priority: HIGH.",
            "severity": "HIGH",
            "metadata": {"risk_score": 84.5, "priority": "HIGH", "model": "XGBoost v2.1", "auc": 0.91},
        },
        {
            "event_type": "NOTICE_ISSUED",
            "timestamp": "2024-07-05T14:00:00",
            "date_label": "5 Jul 2024",
            "actor": "Labour Inspector — INS-OFFICER-37",
            "actor_type": "INSPECTOR",
            "title": "Statutory Clarification Notice Issued",
            "description": "Inspector issued written notice under Code on Wages 2019 Section 50 requesting the employer to furnish explanation for the 5-worker headcount gap within 7 working days.",
            "severity": "MEDIUM",
            "metadata": {"notice_ref": "CLR-2024-PUN-0041", "deadline_days": 7},
        },
        {
            "event_type": "REMEDIATION_SUBMITTED",
            "timestamp": "2024-07-10T11:22:00",
            "date_label": "10 Jul 2024",
            "actor": "ABC Industries Compliance Officer",
            "actor_type": "EMPLOYER",
            "title": "Employer Response to Clarification Notice",
            "description": "Employer submitted contractor invoice showing 5 workers engaged through ABC Manpower Services Pvt Ltd. Payroll reconciliation scroll uploaded showing matching UTR transfers.",
            "severity": "INFO",
            "metadata": {"notice_ref": "CLR-2024-PUN-0041", "documents_uploaded": 2},
        },
        {
            "event_type": "DOCUMENT_SUBMITTED",
            "timestamp": "2024-10-01T08:45:00",
            "date_label": "1 Oct 2024",
            "actor": "ABC Industries HR Portal",
            "actor_type": "EMPLOYER",
            "title": "Q2 Statutory Register Submission",
            "description": "Employer submitted Q2 2024 registers including updated Form B, Form D, and Bank UTR Scroll. Safety Committee meeting minutes for July-September not included.",
            "severity": "LOW",
            "metadata": {"documents": ["Form B", "Form D", "Bank UTR Scroll"], "missing": ["Safety Committee Minutes"]},
        },
        {
            "event_type": "COMPLIANCE_EVALUATED",
            "timestamp": "2024-10-01T09:15:00",
            "date_label": "1 Oct 2024",
            "actor": "ShramAI Document Agent",
            "actor_type": "SYSTEM",
            "title": "Q2 Evaluation: 2 Issues Detected",
            "description": "Form B Q2 shows ₹340/day wage shortfall for 3 unskilled helpers vs. notified State Minimum Wage (Code on Wages). Safety Committee meeting minutes missing for Q2.",
            "severity": "HIGH",
            "metadata": {"wage_shortfall_inr": 340, "workers_affected": 3, "missing_docs": 1},
        },
        {
            "event_type": "RISK_ASSESSED",
            "timestamp": "2024-10-01T09:16:00",
            "date_label": "1 Oct 2024",
            "actor": "XGBoost ML Risk Model v2.1",
            "actor_type": "ML_ENGINE",
            "title": "Risk Score Revised Upward: 91.2 / 100",
            "description": "Recurring wage violation in Q2 triggered score escalation to 91.2. Establishment entered Top 5% risk percentile. Priority escalated to CRITICAL for immediate inspection scheduling.",
            "severity": "CRITICAL",
            "metadata": {"risk_score": 91.2, "priority": "CRITICAL", "percentile": "Top 5%"},
        },
        {
            "event_type": "INSPECTION_SCHEDULED",
            "timestamp": "2024-10-03T10:00:00",
            "date_label": "3 Oct 2024",
            "actor": "Central Inspection Scheduler — INS-OFFICER-42",
            "actor_type": "INSPECTOR",
            "title": "Field Inspection Scheduled via Batch Dispatch",
            "description": "Establishment selected as Rank #1 in multi-criteria prioritization queue. Inspection scheduled for 15 October 2024 under 72-hour target window. Composite Priority Score: 91.2.",
            "severity": "HIGH",
            "metadata": {"inspector_id": "INS-OFFICER-42", "scheduled_date": "2024-10-15", "priority_rank": 1},
        },
        {
            "event_type": "VIOLATION_DETECTED",
            "timestamp": "2024-10-15T11:30:00",
            "date_label": "15 Oct 2024",
            "actor": "Inspector INS-OFFICER-42 — On-Site Inspection",
            "actor_type": "INSPECTOR",
            "title": "On-Site Inspection Completed — 3 Violations Confirmed",
            "description": "Physical inspection confirmed: (1) Form B wage entries below statutory floor for Shift B — ₹7,800 total arrears; (2) Safety Committee not constituted per OSHWC Code 2020 §23; (3) Overtime authorization register absent.",
            "severity": "CRITICAL",
            "metadata": {"violations": 3, "session_id": "INSP-A7B2C3D4", "total_penalty_proposed_inr": 120000},
        },
        {
            "event_type": "PENALTY_PROPOSED",
            "timestamp": "2024-10-15T14:00:00",
            "date_label": "15 Oct 2024",
            "actor": "Inspector INS-OFFICER-42",
            "actor_type": "INSPECTOR",
            "title": "Penalty Docket Filed — ₹1,20,000 Proposed",
            "description": "Violation docket submitted: §54(1) Code on Wages — ₹50,000; OSHWC §96 — ₹50,000; §54(2) Overtime Register — ₹20,000. 14-day safe harbour window granted for voluntary remediation.",
            "severity": "CRITICAL",
            "metadata": {"penalty_inr": 120000, "report_ref": "RPT-A7B2C3D4", "safe_harbour_days": 14},
        },
        {
            "event_type": "REMEDIATION_SUBMITTED",
            "timestamp": "2024-10-28T09:00:00",
            "date_label": "28 Oct 2024",
            "actor": "ABC Industries Compliance Officer",
            "actor_type": "EMPLOYER",
            "title": "Remediation Proof Submitted within Safe Harbour",
            "description": "Employer submitted: (1) Wage differential payment UTRs for ₹7,800 to 3 workers; (2) Safety Committee constitution notice signed by management; (3) Overtime Authorization Register (Form Q) for Oct 2024.",
            "severity": "INFO",
            "metadata": {"arrears_paid_inr": 7800, "safe_harbour_used": True},
        },
        {
            "event_type": "SAFE_HARBOUR_ACHIEVED",
            "timestamp": "2024-10-30T16:00:00",
            "date_label": "30 Oct 2024",
            "actor": "ShramAI Compliance Review Engine",
            "actor_type": "SYSTEM",
            "title": "Safe Harbour Verified — Penalties Waived",
            "description": "All 3 violations remediated within the statutory safe harbour window. Penalty waived per Code on Wages 2019 safe harbour provisions. Establishment compliance score revised to 68 / 100.",
            "severity": "INFO",
            "metadata": {"penalty_waived_inr": 120000, "new_compliance_score": 68},
        },
    ],
    "EST-002": [
        {
            "event_type": "DOCUMENT_SUBMITTED",
            "timestamp": "2024-06-15T10:00:00",
            "date_label": "15 Jun 2024",
            "actor": "Bharat Garments Compliance Portal",
            "actor_type": "EMPLOYER",
            "title": "Annual Register Submission",
            "description": "Submitted Form A, Form B, Form D and ESIC challan for 2023-24.",
            "severity": "INFO",
            "metadata": {},
        },
        {
            "event_type": "RISK_ASSESSED",
            "timestamp": "2024-06-15T11:00:00",
            "date_label": "15 Jun 2024",
            "actor": "XGBoost ML Risk Model v2.1",
            "actor_type": "ML_ENGINE",
            "title": "ML Risk Score: 58.2 / 100 (MEDIUM)",
            "description": "Establishment scored MEDIUM risk. Minor anomaly in EPF contribution timing noted but within acceptable variance.",
            "severity": "MEDIUM",
            "metadata": {"risk_score": 58.2, "priority": "MEDIUM"},
        },
    ],
}


class TimelineService:

    @classmethod
    def get_establishment_timeline(cls, establishment_id: str) -> EstablishmentTimeline:
        raw_events = TIMELINE_DATA.get(establishment_id, TIMELINE_DATA["EST-001"])

        events = []
        for i, ev in enumerate(raw_events):
            events.append(TimelineEvent(
                event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
                **ev,
            ))

        name_map = {
            "EST-001": "ABC Industries Ltd.",
            "EST-002": "Bharat Garments Pvt Ltd",
            "EST-003": "ChemTech Processing Unit",
        }

        return EstablishmentTimeline(
            establishment_id=establishment_id,
            establishment_name=name_map.get(establishment_id, "Unknown Establishment"),
            total_events=len(events),
            first_audit_date=events[0].date_label if events else "N/A",
            last_activity_date=events[-1].date_label if events else "N/A",
            events=events,
        )
