from app.agents.compliance_agent import ComplianceAgentService


def test_compliance_agent_audit_pipeline():
    result = ComplianceAgentService.run_compliance_audit(
        establishment_id="EST-001",
        worker_count=420,
    )
    assert result.establishment_id == "EST-001"
    assert result.total_rules_evaluated >= 5
    assert result.violations_count >= 1
    assert result.compliance_score > 0.0

    # Inspect first grounded finding
    finding = result.findings[0]
    assert finding.status == "FAILED"
    assert finding.severity in ["HIGH", "MEDIUM", "LOW"]
    assert len(finding.explanation) > 20

    # Verify Evidence Anchor
    anchor = finding.evidence_anchor
    assert anchor.document_name is not None
    assert anchor.page_number >= 1
    assert len(anchor.discrepancy_value) > 5

    # Verify RAG Statutory Enrichment
    statutory = finding.statutory_enrichment
    assert "Code" in statutory.act_title
    assert "Section" in statutory.section_number
    assert len(statutory.statutory_quote) > 10
    assert statutory.relevance_score >= 0.70

    # Verify Actionable Remedy
    assert len(finding.actionable_remedy) > 10


def test_compliance_agent_zero_hallucination_guarantee():
    result = ComplianceAgentService.run_compliance_audit(establishment_id="EST-001")
    allowed_acts = {
        "The Code on Wages, 2019",
        "The Industrial Relations Code, 2020",
        "The Code on Social Security, 2020",
        "The Occupational Safety, Health and Working Conditions Code, 2020",
        "The OSHWC Code, 2020",
    }
    for finding in result.findings:
        assert finding.statutory_enrichment.act_title in allowed_acts
        assert finding.statutory_enrichment.section_number.startswith("Section")


def test_compliance_agent_api_endpoint(client):
    response = client.post("/api/v1/agents/compliance/audit?establishment_id=EST-001")
    assert response.status_code == 200
    data = response.json()
    assert data["establishment_id"] == "EST-001"
    assert len(data["findings"]) >= 1
    assert "agent_summary" in data
    assert any(f["rule_id"] == "MIN_WAGE_001" for f in data["findings"])
