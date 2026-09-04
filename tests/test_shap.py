from app.ml.shap_explainer import ShapExplainerService


def test_tree_shap_local_explanation():
    res = ShapExplainerService.explain_establishment(
        establishment_id="EST-001",
        worker_count=420,
        contract_worker_ratio=0.55,
        hazardous_process=True,
        wage_violation_count=3,
        ghost_worker_count=1,
    )
    assert res.establishment_id == "EST-001"
    assert 30.0 <= res.base_value <= 70.0
    assert 10.0 <= res.predicted_risk_score <= 100.0
    assert len(res.all_contributions) == 22

    # Check positive escalators
    assert len(res.positive_escalators) >= 1
    for esc in res.positive_escalators:
        assert esc.shap_value > 0.0
        assert esc.direction == "positive"
        assert len(esc.explanation) > 5

    # Check negative mitigators if any
    for mit in res.negative_mitigators:
        assert mit.shap_value < 0.0
        assert mit.direction == "negative"


def test_shap_global_importance():
    res = ShapExplainerService.compute_global_importance(max_samples=50)
    assert res.feature_count == 22
    assert res.dataset_size == 50
    assert len(res.top_features) == 22

    # Check ranking
    assert res.top_features[0].rank == 1
    assert res.top_features[0].mean_abs_shap >= res.top_features[-1].mean_abs_shap


def test_shap_api_endpoints(client):
    # POST explain
    exp_resp = client.post(
        "/api/v1/ml/shap/explain",
        json={"establishment_id": "EST-001", "worker_count": 300, "hazardous_process": True},
    )
    assert exp_resp.status_code == 200
    exp_data = exp_resp.json()
    assert exp_data["establishment_id"] == "EST-001"
    assert "base_value" in exp_data
    assert len(exp_data["positive_escalators"]) >= 1

    # GET global-importance
    glob_resp = client.get("/api/v1/ml/shap/global-importance?max_samples=30")
    assert glob_resp.status_code == 200
    glob_data = glob_resp.json()
    assert glob_data["feature_count"] == 22
    assert len(glob_data["top_features"]) == 22
