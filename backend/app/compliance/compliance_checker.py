from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.schemas.compliance import (
    ComplianceAuditReport,
    RuleEvaluationFinding,
    RuleStatus,
)
from app.compliance.rule_engine import ComplianceRuleEngine


class ComplianceCheckerService:
    @classmethod
    def run_establishment_audit(
        cls,
        establishment_id: str,
        wage_records: Optional[List[Dict[str, Any]]] = None,
        attendance_records: Optional[List[Dict[str, Any]]] = None,
        uploaded_categories: Optional[List[str]] = None,
        worker_count: int = 420,
        has_safety_record: bool = False,
    ) -> ComplianceAuditReport:
        """
        Executes full deterministic compliance audit across all statutory rules.
        """
        ComplianceRuleEngine.load_rules()

        # Seed sample canonical wage records if none supplied
        if wage_records is None:
            wage_records = [
                {"employee_id": "EMP-001", "employee_name": "Ramesh Kumar", "daily_wage_rate": 650.0, "gross_wages": 18200.0, "total_deductions": 2000.0, "overtime_hours": 8.0, "overtime_wages": 1300.0},
                {"employee_id": "EMP-002", "employee_name": "Sunita Devi", "daily_wage_rate": 550.0, "gross_wages": 14500.0, "total_deductions": 1500.0, "overtime_hours": 0.0, "overtime_wages": 0.0},
                {"employee_id": "EMP-003", "employee_name": "Rajesh K. (Helper)", "daily_wage_rate": 310.0, "gross_wages": 8060.0, "total_deductions": 800.0, "overtime_hours": 12.0, "overtime_wages": 450.0},
                {"employee_id": "EMP-004", "employee_name": "Amit Verma", "daily_wage_rate": 720.0, "gross_wages": 19000.0, "total_deductions": 2000.0, "overtime_hours": 0.0, "overtime_wages": 0.0},
            ]

        if uploaded_categories is None:
            uploaded_categories = ["Wage Register", "Attendance Register"]

        findings: List[RuleEvaluationFinding] = []

        # 1. Minimum Wage Rule
        findings.append(ComplianceRuleEngine.evaluate_minimum_wages(wage_records))

        # 2. Overtime Double Rate Rule
        findings.append(ComplianceRuleEngine.evaluate_overtime_rate(wage_records))

        # 3. Deduction 50% Ceiling Rule
        findings.append(ComplianceRuleEngine.evaluate_deduction_cap(wage_records))

        # 4. Mandatory Registers Rule
        findings.append(ComplianceRuleEngine.evaluate_mandatory_registers(uploaded_categories))

        # 5. Safety Committee Rule
        findings.append(ComplianceRuleEngine.evaluate_safety_committee(worker_count, has_safety_record))

        total_rules = len(findings)
        passed_count = sum(1 for f in findings if f.status == RuleStatus.PASSED)
        failed_count = sum(1 for f in findings if f.status == RuleStatus.FAILED)
        warning_count = sum(1 for f in findings if f.status == RuleStatus.WARNING)

        compliance_score = round((passed_count / total_rules) * 100.0, 1) if total_rules > 0 else 100.0

        return ComplianceAuditReport(
            establishment_id=establishment_id,
            audit_timestamp=datetime.now(timezone.utc).isoformat(),
            total_rules_evaluated=total_rules,
            passed_count=passed_count,
            failed_count=failed_count,
            warning_count=warning_count,
            overall_compliance_score=compliance_score,
            findings=findings,
        )


ComplianceChecker = ComplianceCheckerService
