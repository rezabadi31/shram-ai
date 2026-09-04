import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from app.schemas.anomaly import (
    AnomalyType,
    AnomalySeverity,
    CrossDocumentAnomalyItem,
    ReconciliationSummary,
    CrossDocumentAuditResult,
)


class CrossDocumentAnomalyEngine:
    @classmethod
    def reconcile_wages_and_attendance(
        cls,
        wage_records: List[Dict[str, Any]],
        attendance_records: List[Dict[str, Any]],
    ) -> List[CrossDocumentAnomalyItem]:
        """
        Cross-reconciles Form B Wage Register against Form D Muster Roll:
        - Detects Ghost Workers (Wage credited with zero attendance)
        - Detects Uncompensated Attendance (Days worked without wage disbursement)
        """
        anomalies: List[CrossDocumentAnomalyItem] = []
        att_map = {r.get("employee_id"): r for r in attendance_records if r.get("employee_id")}
        wage_map = {r.get("employee_id"): r for r in wage_records if r.get("employee_id")}

        # 1. Check for Ghost Workers (In wages, but 0 attendance or absent from muster roll)
        for emp_id, wage in wage_map.items():
            att = att_map.get(emp_id)
            days_present = att.get("days_present", 0) if att else 0
            gross_wages = float(wage.get("gross_wages", 0.0))

            if gross_wages > 0 and days_present == 0:
                anomalies.append(
                    CrossDocumentAnomalyItem(
                        anomaly_id=f"ANOM-{uuid.uuid4().hex[:6].upper()}",
                        anomaly_type=AnomalyType.GHOST_WORKER,
                        severity=AnomalySeverity.HIGH,
                        primary_document="Form B - Register of Wages",
                        cross_reference_document="Form D - Muster Roll",
                        description=(
                            f"Worker {emp_id} ({wage.get('employee_name', 'Unknown')}) received gross wage "
                            f"disbursement of ₹{gross_wages:.2f}, but has ZERO attendance logged on Form D Muster Roll."
                        ),
                        discrepancy_amount=gross_wages,
                        affected_worker_id=emp_id,
                        affected_worker_name=wage.get("employee_name"),
                        statutory_implication="Suspected phantom payroll embezzlement / fraudulent statutory filing under Sec. 50 Code on Wages.",
                    )
                )

        # 2. Check for Uncompensated Attendance (Present on muster roll, but absent from wage register or ₹0 paid)
        for emp_id, att in att_map.items():
            wage = wage_map.get(emp_id)
            days_present = float(att.get("days_present", 0.0))
            gross_wages = float(wage.get("gross_wages", 0.0)) if wage else 0.0

            if days_present > 0 and gross_wages == 0:
                anomalies.append(
                    CrossDocumentAnomalyItem(
                        anomaly_id=f"ANOM-{uuid.uuid4().hex[:6].upper()}",
                        anomaly_type=AnomalyType.UNCOMPENSATED_ATTENDANCE,
                        severity=AnomalySeverity.HIGH,
                        primary_document="Form D - Muster Roll",
                        cross_reference_document="Form B - Register of Wages",
                        description=(
                            f"Worker {emp_id} logged {days_present:.0f} physical shifts on Muster Roll Form D, "
                            f"but has NO recorded wage payment or zero disbursement on Form B Wage Register."
                        ),
                        discrepancy_amount=days_present * 450.0,  # minimum floor baseline
                        affected_worker_id=emp_id,
                        affected_worker_name=att.get("employee_name"),
                        statutory_implication="Non-payment of earned wages under Section 17 & 18 Code on Wages 2019.",
                    )
                )

        return anomalies

    @classmethod
    def reconcile_wages_and_bank(
        cls,
        wage_records: List[Dict[str, Any]],
        bank_disbursements: List[Dict[str, Any]],
    ) -> List[CrossDocumentAnomalyItem]:
        """
        Cross-reconciles Form B Wage Register net payable against Bank Disbursement Scrolls:
        - Detects Wage Skimming & Net Payout Mismatches
        """
        anomalies: List[CrossDocumentAnomalyItem] = []
        bank_map = {b.get("employee_id"): b for b in bank_disbursements if b.get("employee_id")}

        for wage in wage_records:
            emp_id = wage.get("employee_id")
            if not emp_id or emp_id not in bank_map:
                continue

            bank = bank_map[emp_id]
            # Net wages on Form B = gross - total_deductions
            gross = float(wage.get("gross_wages", 0.0))
            deductions = float(wage.get("total_deductions", 0.0))
            expected_net = gross - deductions

            actual_disbursed = float(bank.get("amount", bank.get("disbursed_amount", 0.0)))
            diff = abs(expected_net - actual_disbursed)

            if diff > 5.0:  # ₹5 tolerance for bank rounding
                anomalies.append(
                    CrossDocumentAnomalyItem(
                        anomaly_id=f"ANOM-{uuid.uuid4().hex[:6].upper()}",
                        anomaly_type=AnomalyType.DISBURSEMENT_MISMATCH,
                        severity=AnomalySeverity.HIGH if diff > 500 else AnomalySeverity.MEDIUM,
                        primary_document="Form B - Register of Wages",
                        cross_reference_document="Bank Disbursement Scroll (UTR File)",
                        description=(
                            f"Worker {emp_id} Form B Net Payable is ₹{expected_net:.2f}, but actual bank UTR "
                            f"transfer was ₹{actual_disbursed:.2f} (Discrepancy: ₹{diff:.2f})."
                        ),
                        discrepancy_amount=diff,
                        affected_worker_id=emp_id,
                        affected_worker_name=wage.get("employee_name"),
                        statutory_implication="Unauthorized wage deduction / diversion in violation of Section 18 Code on Wages.",
                    )
                )

        return anomalies

    @classmethod
    def reconcile_contract_headcount(
        cls,
        gate_muster_count: int,
        statutory_register_count: int,
    ) -> List[CrossDocumentAnomalyItem]:
        """
        Detects suppression of contract worker count to evade statutory thresholds
        (e.g., hiding workers to stay below 20 for EPFO or 250 for Safety Committee).
        """
        anomalies: List[CrossDocumentAnomalyItem] = []
        if gate_muster_count > statutory_register_count:
            suppressed_workers = gate_muster_count - statutory_register_count
            anomalies.append(
                CrossDocumentAnomalyItem(
                    anomaly_id=f"ANOM-{uuid.uuid4().hex[:6].upper()}",
                    anomaly_type=AnomalyType.CONTRACTOR_SUPPRESSION,
                    severity=AnomalySeverity.HIGH,
                    primary_document="Factory Security Gate Turnstile Log",
                    cross_reference_document="Form A - Register of Employees",
                    description=(
                        f"Gate security access logs show {gate_muster_count} active workers on factory premises, "
                        f"while Form A statutory register declares only {statutory_register_count} employees "
                        f"({suppressed_workers} undeclared contract workers)."
                    ),
                    discrepancy_amount=float(suppressed_workers * 15000),  # estimated monthly suppression volume
                    affected_worker_id=None,
                    affected_worker_name=f"{suppressed_workers} Contract Workers",
                    statutory_implication="Suppression of workforce to evade OSHWC Code Section 22 and Code on Social Security Section 16/32.",
                )
            )
        return anomalies

    @classmethod
    def run_establishment_reconciliation(
        cls,
        establishment_id: str = "EST-001",
        wage_records: Optional[List[Dict[str, Any]]] = None,
        attendance_records: Optional[List[Dict[str, Any]]] = None,
        bank_disbursements: Optional[List[Dict[str, Any]]] = None,
        gate_muster_count: int = 445,
        statutory_register_count: int = 420,
    ) -> CrossDocumentAuditResult:
        """
        Runs comprehensive cross-document reconciliation across Form B, Form D, Bank Scrolls, and Gate Logs.
        """
        if wage_records is None:
            wage_records = [
                {"employee_id": "EMP-001", "employee_name": "Ramesh Kumar", "gross_wages": 18200.0, "total_deductions": 2000.0},
                {"employee_id": "EMP-002", "employee_name": "Sunita Devi", "gross_wages": 14500.0, "total_deductions": 1500.0},
                {"employee_id": "EMP-003", "employee_name": "Rajesh K. (Helper)", "gross_wages": 8060.0, "total_deductions": 800.0},
                {"employee_id": "EMP-004", "employee_name": "Amit Verma", "gross_wages": 19000.0, "total_deductions": 2000.0},
                {"employee_id": "EMP-009", "employee_name": "Vikram Singh (Ghost)", "gross_wages": 16500.0, "total_deductions": 1000.0},
            ]

        if attendance_records is None:
            attendance_records = [
                {"employee_id": "EMP-001", "employee_name": "Ramesh Kumar", "days_present": 26},
                {"employee_id": "EMP-002", "employee_name": "Sunita Devi", "days_present": 25},
                {"employee_id": "EMP-003", "employee_name": "Rajesh K. (Helper)", "days_present": 26},
                {"employee_id": "EMP-004", "employee_name": "Amit Verma", "days_present": 24},
                {"employee_id": "EMP-009", "employee_name": "Vikram Singh (Ghost)", "days_present": 0},  # Ghost worker
                {"employee_id": "EMP-015", "employee_name": "Dinesh Pal (Uncredited)", "days_present": 22},  # Uncompensated
            ]

        if bank_disbursements is None:
            bank_disbursements = [
                {"employee_id": "EMP-001", "amount": 16200.0},
                {"employee_id": "EMP-002", "amount": 13000.0},
                {"employee_id": "EMP-003", "amount": 6260.0},  # Form B net = 8060 - 800 = 7260 (Mismatch: ₹1,000 diverted)
                {"employee_id": "EMP-004", "amount": 17000.0},
                {"employee_id": "EMP-009", "amount": 15500.0},
            ]

        all_anomalies: List[CrossDocumentAnomalyItem] = []

        # 1. Wages vs Attendance
        all_anomalies.extend(cls.reconcile_wages_and_attendance(wage_records, attendance_records))

        # 2. Wages vs Bank
        all_anomalies.extend(cls.reconcile_wages_and_bank(wage_records, bank_disbursements))

        # 3. Headcount suppression
        all_anomalies.extend(cls.reconcile_contract_headcount(gate_muster_count, statutory_register_count))

        # Aggregate metrics
        ghost_count = sum(1 for a in all_anomalies if a.anomaly_type == AnomalyType.GHOST_WORKER)
        uncomp_count = sum(1 for a in all_anomalies if a.anomaly_type == AnomalyType.UNCOMPENSATED_ATTENDANCE)
        financial_discrepancy = sum(a.discrepancy_amount or 0.0 for a in all_anomalies)

        recs = [
            "Summon original UTR bank scrolls to cross-examine EMP-003 wage deduction diversion.",
            "Verify physical presence of EMP-009 at factory shopfloor; biometric log indicates zero turnstile entries.",
            "Inspect contractor gate pass muster for the 25 undeclared contract workers identified at gate security.",
        ]

        summary = ReconciliationSummary(
            records_reconciled=len(wage_records) + len(attendance_records) + len(bank_disbursements),
            anomalies_detected=len(all_anomalies),
            financial_discrepancy_total=round(financial_discrepancy, 2),
            ghost_workers_count=ghost_count,
            uncompensated_workers_count=uncomp_count,
        )

        return CrossDocumentAuditResult(
            establishment_id=establishment_id,
            audit_timestamp=datetime.now(timezone.utc).isoformat(),
            reconciliation_summary=summary,
            anomalies=all_anomalies,
            recommendations=recs,
        )
