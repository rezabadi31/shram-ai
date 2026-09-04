from app.agents.risk_agent import RiskAgentService


def test_risk_agent_evaluate_high_risk():
    res = RiskAgentService.evaluate_establishment_risk(
        establishment_id="EST-001",
        worker_count=450,
        contract_worker_ratio=0.60,
        hazardous_process=True,
        wage_violation_count=4,
        ghost_worker_count=2,
        missing_register_count=2,
    )
    assert res.establishment_id == "EST-001"
    assert "XGBoost" in res.ml_model_used
    assert res.calibrated_risk_score >= 70.0
    assert res.priority_class == "HIGH"
    assert res.confidence_score >= 0.85
    assert len(res.enforcement_directives) >= 2

    # Check emergency directive
    action_types = [d.action_type for d in res.enforcement_directives]
    assert "PHYSICAL_SURPRISE_INSPECTION" in action_types
    assert any(d.urgency == "IMMEDIATE_72H" for d in res.enforcement_directives)

    # Check attribution synthesis
    assert len(res.attribution_synthesis.top_escalators) >= 1
    assert "HIGH INSPECTION PRIORITY" in res.attribution_synthesis.synthesis_narrative


def test_risk_agent_evaluate_low_risk():
    res = RiskAgentService.evaluate_establishment_risk(
        establishment_id="EST-099",
        worker_count=25,
        contract_worker_ratio=0.05,
        hazardous_process=False,
        wage_violation_count=0,
        ot_violation_count=0,
        deduction_violation_count=0,
        missing_register_count=0,
        ghost_worker_count=0,
        uncompensated_worker_count=0,
        disbursement_mismatch_count=0,
    )
    assert res.calibrated_risk_score < 60.0
    assert res.priority_class in ["MEDIUM", "LOW"]


def test_risk_agent_api_endpoints(client):
    # POST evaluate
    eval_resp = client.post(
        "/api/v1/agents/risk/evaluate",
        json={"establishment_id": "EST-001", "worker_count": 300, "hazardous_process": True},
    )
    assert eval_resp.status_code == 200
    data = eval_resp.json()
    assert data["establishment_id"] == "EST-001"
    assert "calibrated_risk_score" in data
    assert "priority_class" in data
    assert len(data["enforcement_directives"]) >= 1

    # GET thresholds
    thresh_resp = client.get("/api/v1/agents/risk/thresholds")
    assert thresh_resp.status_code == 200
    thresh_data = thresh_resp.json()
    assert thresh_data["high_threshold"] == 75.0
    assert thresh_data["medium_threshold"] == 40.0
