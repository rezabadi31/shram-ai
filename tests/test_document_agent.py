from app.agents.document_agent import DocumentAgentService
from app.schemas.document_agent import LegibilityStatus, RegisterFilingStatus


def test_evaluate_legibility_scoring():
    docs_high = [{"ocr_confidence": 0.96}, {"ocr_confidence": 0.94}]
    score, status = DocumentAgentService.evaluate_legibility(docs_high)
    assert score == 95.0
    assert status == LegibilityStatus.EXCELLENT

    docs_low = [{"ocr_confidence": 0.55}, {"ocr_confidence": 0.50}]
    score_low, status_low = DocumentAgentService.evaluate_legibility(docs_low)
    assert score_low < 60.0
    assert status_low == LegibilityStatus.UNREADABLE


def test_determine_required_registers_thresholds():
    # Large factory (420 workers)
    large_reqs = DocumentAgentService.determine_required_registers(worker_count=420)
    reg_ids = {r["register_id"] for r in large_reqs}
    assert "REG_FORM_A" in reg_ids
    assert "REG_FORM_B" in reg_ids
    assert "REG_FORM_C" in reg_ids
    assert "REG_FORM_D" in reg_ids
    assert "REG_EPFO_ECR" in reg_ids
    assert "REG_ESIC_FORM5" in reg_ids
    assert "REG_SAFETY_LOG" in reg_ids
    assert len(large_reqs) == 7

    # Small enterprise (15 workers)
    small_reqs = DocumentAgentService.determine_required_registers(worker_count=15)
    small_ids = {r["register_id"] for r in small_reqs}
    assert "REG_EPFO_ECR" not in small_ids  # Requires 20+
    assert "REG_SAFETY_LOG" not in small_ids  # Requires 250+
    assert "REG_ESIC_FORM5" in small_ids  # Requires 10+


def test_document_audit_gap_analysis():
    # Uploaded has Wage Register, Attendance, Form A, and Bank Scroll
    # Missing Form C (Deductions) and Safety Log
    audit = DocumentAgentService.run_document_audit(
        establishment_id="EST-001",
        worker_count=420,
    )
    assert audit.submitted_count >= 3
    assert audit.missing_count >= 1
    assert audit.overall_legibility_score >= 90.0

    missing_regs = [r for r in audit.register_comparisons if r.status == RegisterFilingStatus.MISSING]
    missing_names = {r.form_designation for r in missing_regs}
    assert "Form C" in missing_names
    assert len(audit.missing_registers_penalties) >= 1
    assert "summons" in audit.agent_recommendation.lower()


def test_document_agent_api_endpoints(client):
    # Test GET required-registers
    response = client.get("/api/v1/agents/document/required-registers?worker_count=420")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 7

    # Test POST audit
    audit_resp = client.post("/api/v1/agents/document/audit?establishment_id=EST-001")
    assert audit_resp.status_code == 200
    audit_data = audit_resp.json()
    assert audit_data["establishment_id"] == "EST-001"
    assert "register_comparisons" in audit_data
    assert audit_data["total_required_registers"] == 7
