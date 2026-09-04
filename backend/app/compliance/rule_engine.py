import os
import json
from typing import List, Dict, Any, Tuple
from app.schemas.compliance import (
    RuleDefinition,
    RuleEvaluationFinding,
    RuleStatus,
    RuleSeverity,
    StatutoryRuleCategory,
)

RULES_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "rules", "statutory_rules.json")
)


class ComplianceRuleEngine:
    _rules: List[RuleDefinition] = []
    _loaded = False

    @classmethod
    def load_rules(cls) -> List[RuleDefinition]:
        if cls._loaded:
            return cls._rules

        if os.path.exists(RULES_FILE):
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                cls._rules = [RuleDefinition(**r) for r in data]
        cls._loaded = True
        return cls._rules

    @classmethod
    def evaluate_minimum_wages(cls, wage_records: List[Dict[str, Any]], floor_rate: float = 450.0) -> RuleEvaluationFinding:
        """Evaluates MIN_WAGE_001: daily_wage_rate >= floor_rate."""
        violating_ids = []
        worst_delta = 0.0
        worst_emp = ""

        for rec in wage_records:
            rate = float(rec.get("daily_wage_rate", 0.0))
            if rate < floor_rate:
                emp_id = rec.get("employee_id", "Unknown")
                violating_ids.append(emp_id)
                delta = floor_rate - rate
                if delta > worst_delta:
                    worst_delta = delta
                    worst_emp = f"{emp_id} ({rec.get('employee_name', 'Worker')}) received ₹{rate:.2f}/day (deficit ₹{delta:.2f}/day)"

        if violating_ids:
            return RuleEvaluationFinding(
                rule_id="MIN_WAGE_001",
                rule_name="Statutory Minimum Wage Rate Floor Check",
                status=RuleStatus.FAILED,
                severity=RuleSeverity.HIGH,
                statutory_reference="Code on Wages, 2019, Section 6 & Section 8",
                authority="Chief Labour Commissioner (Central)",
                evidence=f"{len(violating_ids)} worker(s) paid below national floor ₹{floor_rate:.2f}/day. Worst violation: {worst_emp}.",
                affected_entities_count=len(violating_ids),
                affected_entity_ids=violating_ids,
            )
        return RuleEvaluationFinding(
            rule_id="MIN_WAGE_001",
            rule_name="Statutory Minimum Wage Rate Floor Check",
            status=RuleStatus.PASSED,
            severity=RuleSeverity.HIGH,
            statutory_reference="Code on Wages, 2019, Section 6 & Section 8",
            authority="Chief Labour Commissioner (Central)",
            evidence="All audited employees remunerated at or above statutory minimum floor rate.",
        )

    @classmethod
    def evaluate_overtime_rate(cls, wage_records: List[Dict[str, Any]]) -> RuleEvaluationFinding:
        """Evaluates OVERTIME_001: overtime pay >= 2x normal rate."""
        violating_ids = []
        example_violation = ""

        for rec in wage_records:
            ot_hours = float(rec.get("overtime_hours", 0.0))
            if ot_hours > 0:
                daily_rate = float(rec.get("daily_wage_rate", 0.0))
                hourly_rate = daily_rate / 8.0
                required_ot_pay = ot_hours * hourly_rate * 2.0
                actual_ot_pay = float(rec.get("overtime_wages", 0.0))

                # If underpaid by more than ₹10
                if (required_ot_pay - actual_ot_pay) > 10.0:
                    emp_id = rec.get("employee_id", "Unknown")
                    violating_ids.append(emp_id)
                    if not example_violation:
                        example_violation = f"{emp_id} worked {ot_hours:.1f} OT hrs, paid ₹{actual_ot_pay:.2f} vs statutory double rate ₹{required_ot_pay:.2f}"

        if violating_ids:
            return RuleEvaluationFinding(
                rule_id="OVERTIME_001",
                rule_name="Statutory Overtime Double Rate Verification",
                status=RuleStatus.FAILED,
                severity=RuleSeverity.HIGH,
                statutory_reference="Code on Wages, 2019, Section 14",
                authority="Inspector-cum-Facilitator",
                evidence=f"{len(violating_ids)} worker(s) underpaid for statutory overtime. Example: {example_violation}.",
                affected_entities_count=len(violating_ids),
                affected_entity_ids=violating_ids,
            )
        return RuleEvaluationFinding(
            rule_id="OVERTIME_001",
            rule_name="Statutory Overtime Double Rate Verification",
            status=RuleStatus.PASSED,
            severity=RuleSeverity.HIGH,
            statutory_reference="Code on Wages, 2019, Section 14",
            authority="Inspector-cum-Facilitator",
            evidence="Overtime remuneration strictly complies with statutory 2x hourly wage rate requirement.",
        )

    @classmethod
    def evaluate_deduction_cap(cls, wage_records: List[Dict[str, Any]]) -> RuleEvaluationFinding:
        """Evaluates DEDUCTION_CAP_001: deductions <= 50% of gross."""
        violating_ids = []
        example = ""

        for rec in wage_records:
            gross = float(rec.get("gross_wages", 0.0))
            deductions = float(rec.get("total_deductions", 0.0))
            if gross > 0 and (deductions / gross) > 0.50:
                emp_id = rec.get("employee_id", "Unknown")
                violating_ids.append(emp_id)
                pct = (deductions / gross) * 100
                if not example:
                    example = f"{emp_id} deductions ₹{deductions:.2f} constituted {pct:.1f}% of gross wages ₹{gross:.2f}"

        if violating_ids:
            return RuleEvaluationFinding(
                rule_id="DEDUCTION_CAP_001",
                rule_name="Statutory Maximum 50% Deduction Ceiling",
                status=RuleStatus.FAILED,
                severity=RuleSeverity.HIGH,
                statutory_reference="Code on Wages, 2019, Section 18(3)",
                authority="Inspector-cum-Facilitator",
                evidence=f"{len(violating_ids)} worker(s) had deductions exceeding statutory 50% ceiling. Example: {example}.",
                affected_entities_count=len(violating_ids),
                affected_entity_ids=violating_ids,
            )
        return RuleEvaluationFinding(
            rule_id="DEDUCTION_CAP_001",
            rule_name="Statutory Maximum 50% Deduction Ceiling",
            status=RuleStatus.PASSED,
            severity=RuleSeverity.HIGH,
            statutory_reference="Code on Wages, 2019, Section 18(3)",
            authority="Inspector-cum-Facilitator",
            evidence="All deductions comply with the statutory 50% aggregate ceiling.",
        )

    @classmethod
    def evaluate_mandatory_registers(cls, uploaded_categories: List[str]) -> RuleEvaluationFinding:
        """Evaluates MANDATORY_REGISTERS_001: Form A, Form B, Form D."""
        required = {"Wage Register", "Attendance Register", "Employee Register"}
        present = set(uploaded_categories)
        missing = required - present

        if missing:
            return RuleEvaluationFinding(
                rule_id="MANDATORY_REGISTERS_001",
                rule_name="Mandatory Statutory Registers Maintenance (Form A, B, D)",
                status=RuleStatus.FAILED,
                severity=RuleSeverity.HIGH,
                statutory_reference="Code on Wages, 2019, Section 50",
                authority="Labour Enforcement Officer",
                evidence=f"Establishment failed to submit mandatory statutory registers: {', '.join(missing)}.",
                affected_entities_count=len(missing),
            )
        return RuleEvaluationFinding(
            rule_id="MANDATORY_REGISTERS_001",
            rule_name="Mandatory Statutory Registers Maintenance (Form A, B, D)",
            status=RuleStatus.PASSED,
            severity=RuleSeverity.HIGH,
            statutory_reference="Code on Wages, 2019, Section 50",
            authority="Labour Enforcement Officer",
            evidence="All prescribed statutory registers (Form A, Form B, Form D) submitted and maintained.",
        )

    @classmethod
    def evaluate_safety_committee(cls, worker_count: int, has_safety_record: bool) -> RuleEvaluationFinding:
        """Evaluates SAFETY_COMMITTEE_001: workforce >= 250 requires safety committee."""
        if worker_count >= 250 and not has_safety_record:
            return RuleEvaluationFinding(
                rule_id="SAFETY_COMMITTEE_001",
                rule_name="Mandatory Bi-partite Safety Committee Constitution",
                status=RuleStatus.FAILED,
                severity=RuleSeverity.HIGH,
                statutory_reference="OSHWC Code, 2020, Section 22",
                authority="Chief Inspector of Factories",
                evidence=f"Factory employs {worker_count} workers (>= 250 threshold) but lacks evidence of an active Bi-partite Safety Committee.",
                affected_entities_count=1,
            )
        return RuleEvaluationFinding(
            rule_id="SAFETY_COMMITTEE_001",
            rule_name="Mandatory Bi-partite Safety Committee Constitution",
            status=RuleStatus.PASSED,
            severity=RuleSeverity.HIGH,
            statutory_reference="OSHWC Code, 2020, Section 22",
            authority="Chief Inspector of Factories",
            evidence="Safety Committee statutory requirements satisfied or establishment headcount below 250 threshold.",
        )


DeterministicRuleEngine = ComplianceRuleEngine
