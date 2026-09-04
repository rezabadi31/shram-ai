from app.compliance.rule_engine import ComplianceRuleEngine
from app.compliance.compliance_checker import ComplianceCheckerService
from app.schemas.compliance import RuleStatus, RuleSeverity


def test_rule_definitions_loading():
    rules = ComplianceRuleEngine.load_rules()
    assert len(rules) >= 5
    rule_ids = {r.rule_id for r in rules}
    assert "MIN_WAGE_001" in rule_ids
    assert "OVERTIME_001" in rule_ids
    assert "DEDUCTION_CAP_001" in rule_ids
    assert "MANDATORY_REGISTERS_001" in rule_ids
    assert "SAFETY_COMMITTEE_001" in rule_ids


def test_minimum_wage_rule_violation():
    wage_records = [
        {"employee_id": "EMP-001", "employee_name": "Ramesh", "daily_wage_rate": 650.0},
        {"employee_id": "EMP-003", "employee_name": "Rajesh (Helper)", "daily_wage_rate": 310.0},
    ]
    finding = ComplianceRuleEngine.evaluate_minimum_wages(wage_records, floor_rate=450.0)
    assert finding.status == RuleStatus.FAILED
    assert finding.severity == RuleSeverity.HIGH
    assert "EMP-003" in finding.affected_entity_ids
    assert "₹310.00" in finding.evidence
    assert finding.statutory_reference == "Code on Wages, 2019, Section 6 & Section 8"


def test_minimum_wage_rule_passing():
    wage_records = [
        {"employee_id": "EMP-001", "employee_name": "Ramesh", "daily_wage_rate": 650.0},
        {"employee_id": "EMP-002", "employee_name": "Sunita", "daily_wage_rate": 550.0},
    ]
    finding = ComplianceRuleEngine.evaluate_minimum_wages(wage_records, floor_rate=450.0)
    assert finding.status == RuleStatus.PASSED
    assert finding.affected_entities_count == 0


def test_overtime_double_rate_rule_violation():
    # 10 OT hours, daily rate 800 (hourly 100). Statutory 2x OT rate = 200/hr. Total OT pay should be 2000.
    # If paid only 1000, underpaid by 1000.
    wage_records = [
        {"employee_id": "EMP-010", "daily_wage_rate": 800.0, "overtime_hours": 10.0, "overtime_wages": 1000.0}
    ]
    finding = ComplianceRuleEngine.evaluate_overtime_rate(wage_records)
    assert finding.status == RuleStatus.FAILED
    assert "EMP-010" in finding.affected_entity_ids
    assert "statutory double rate" in finding.evidence


def test_deduction_cap_50_percent_violation():
    # Gross 10000, deductions 6000 (60% > 50%)
    wage_records = [
        {"employee_id": "EMP-020", "gross_wages": 10000.0, "total_deductions": 6000.0}
    ]
    finding = ComplianceRuleEngine.evaluate_deduction_cap(wage_records)
    assert finding.status == RuleStatus.FAILED
    assert "60.0%" in finding.evidence


def test_mandatory_registers_missing():
    # Only submitted Wage Register, missing Attendance and Employee Registers
    uploaded = ["Wage Register"]
    finding = ComplianceRuleEngine.evaluate_mandatory_registers(uploaded)
    assert finding.status == RuleStatus.FAILED
    assert "Attendance Register" in finding.evidence or "Employee Register" in finding.evidence


def test_safety_committee_threshold():
    # 420 workers without safety record
    finding = ComplianceRuleEngine.evaluate_safety_committee(worker_count=420, has_safety_record=False)
    assert finding.status == RuleStatus.FAILED
    assert "420 workers" in finding.evidence
    assert finding.statutory_reference == "OSHWC Code, 2020, Section 22"


def test_compliance_api_rules_endpoint(client):
    response = client.get("/api/v1/compliance/rules")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    assert any(r["rule_id"] == "MIN_WAGE_001" for r in data)


def test_compliance_api_evaluate_endpoint(client):
    response = client.post("/api/v1/compliance/evaluate?establishment_id=EST-001")
    assert response.status_code == 200
    data = response.json()
    assert data["establishment_id"] == "EST-001"
    assert data["total_rules_evaluated"] == 5
    assert data["failed_count"] >= 1
    assert "findings" in data
    assert any(f["rule_id"] == "MIN_WAGE_001" for f in data["findings"])
