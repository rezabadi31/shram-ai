import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_system_diagnostics_telemetry():
    """
    Tests GET /api/v1/health/diagnostics endpoint.
    Verifies full operational telemetry, all 8 subsystems, statutory coverage, and zero hallucination.
    """
    response = client.get("/api/v1/health/diagnostics")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ALL_SYSTEMS_OPERATIONAL"
    assert data["uptime_seconds"] >= 0
    assert data["zero_hallucination_guarantee"] is True
    assert "ENFORCED" in data["rbac_enforcement_status"]
    assert "ShramAI" in data["model_version"]

    # Verify 8 subsystems
    subsystems = data["subsystems"]
    assert len(subsystems) == 8
    subsystem_names = [s["name"] for s in subsystems]
    expected_names = [
        "Document AI Engine",
        "Compliance Rule Engine",
        "Cross-Document Anomaly Engine",
        "ML Risk Engine",
        "Agent Orchestrator",
        "Labour Law RAG Engine",
        "Safe Harbour Certification Vault",
        "Continuous Drift Monitor",
    ]
    for exp in expected_names:
        assert exp in subsystem_names
    for s in subsystems:
        assert s["status"] == "OPERATIONAL"
        assert s["latency_ms"] >= 0.0
        assert len(s["details"]) > 0

    # Verify 4 Labour Codes statutory coverage
    coverage = data["statutory_coverage"]
    assert len(coverage) == 4
    code_names = [c["code_name"] for c in coverage]
    assert any("Wages" in n for n in code_names)
    assert any("Industrial Relations" in n for n in code_names)
    assert any("Social Security" in n for n in code_names)
    assert any("OSHWC" in n or "Occupational" in n for n in code_names)
    for c in coverage:
        assert c["statutory_sections_count"] > 0
        assert c["rule_templates_count"] > 0
        assert "STATUTORILY AUDITED" in c["coverage_status"]


def test_diagnostic_probe_all():
    """
    Tests POST /api/v1/health/diagnostics/probe with 'all'.
    Ensures active micro-probes test all 8 subsystems deterministically.
    """
    response = client.post("/api/v1/health/diagnostics/probe", json={"subsystem": "all"})
    assert response.status_code == 200
    data = response.json()

    assert data["total_probes"] == 8
    assert data["all_passed"] is True
    results = data["results"]
    assert len(results) == 8

    subsystems_probed = {r["subsystem"] for r in results}
    assert "document_ai" in subsystems_probed
    assert "rule_engine" in subsystems_probed
    assert "cross_document_anomaly" in subsystems_probed
    assert "ml_risk_engine" in subsystems_probed
    assert "agent_orchestrator" in subsystems_probed
    assert "rag_engine" in subsystems_probed
    assert "safe_harbour_vault" in subsystems_probed
    assert "drift_monitor" in subsystems_probed

    for r in results:
        assert r["status"] == "PASSED"
        assert r["latency_ms"] >= 0.0
        assert isinstance(r["output"], dict)


def test_diagnostic_probe_individual_subsystems():
    """
    Tests POST /api/v1/health/diagnostics/probe with targeted individual subsystems.
    """
    # Test document_ai probe
    resp1 = client.post("/api/v1/health/diagnostics/probe", json={"subsystem": "document_ai"})
    assert resp1.status_code == 200
    d1 = resp1.json()
    assert d1["total_probes"] == 1
    assert d1["all_passed"] is True
    assert d1["results"][0]["subsystem"] == "document_ai"
    assert d1["results"][0]["output"]["detected_category"] in ("Wage Register", "WAGE_REGISTER")

    # Test rule_engine probe
    resp2 = client.post("/api/v1/health/diagnostics/probe", json={"subsystem": "rule_engine"})
    assert resp2.status_code == 200
    d2 = resp2.json()
    assert d2["total_probes"] == 1
    assert d2["all_passed"] is True
    assert d2["results"][0]["subsystem"] == "rule_engine"
    assert d2["results"][0]["output"]["affected_count"] == 1

    # Test cross_document_anomaly probe
    resp3 = client.post("/api/v1/health/diagnostics/probe", json={"subsystem": "cross_document_anomaly"})
    assert resp3.status_code == 200
    d3 = resp3.json()
    assert d3["total_probes"] == 1
    assert d3["all_passed"] is True
    assert d3["results"][0]["output"]["anomalies_detected"] >= 1
    assert d3["results"][0]["output"]["first_anomaly_type"] == "GHOST_WORKER"

    # Test safe_harbour_vault probe
    resp4 = client.post("/api/v1/health/diagnostics/probe", json={"subsystem": "safe_harbour_vault"})
    assert resp4.status_code == 200
    d4 = resp4.json()
    assert d4["total_probes"] == 1
    assert d4["all_passed"] is True
    assert d4["results"][0]["output"]["penalty_reduction_inr"] > 0
