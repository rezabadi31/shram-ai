from pathlib import Path
from app.ml.model_trainer import MLRiskModelTrainer


def test_train_and_benchmark_models():
    res = MLRiskModelTrainer.train_and_benchmark()
    assert res.status == "SUCCESS"
    assert res.benchmark.champion_model.startswith("XGBoost")
    assert len(res.benchmark.models) == 3

    # Check that champion model and benchmark json exist
    assert Path("models/champion_risk_model.joblib").exists()
    assert Path("models/benchmark_report.json").exists()

    # Check metrics quality
    for m in res.benchmark.models:
        assert m.roc_auc >= 0.70
        assert m.precision >= 0.60
        assert m.recall >= 0.60
        assert m.f1_score >= 0.60
        assert m.training_time_ms >= 0.0

    # Ensure champion has highest or top tier AUC
    champion_m = next(m for m in res.benchmark.models if m.is_champion)
    assert champion_m.roc_auc >= 0.85


def test_predict_risk_deterministic():
    pred = MLRiskModelTrainer.predict_risk(
        establishment_id="EST-001",
        worker_count=420,
        contract_worker_ratio=0.55,
        hazardous_process=True,
        wage_violation_count=4,
        ghost_worker_count=2,
    )
    assert pred.establishment_id == "EST-001"
    assert "XGBoost" in pred.ml_model
    assert 10.0 <= pred.risk_score <= 100.0
    assert 0.0 <= pred.risk_probability <= 1.0
    assert pred.priority_class in ["HIGH", "MEDIUM", "LOW"]
    assert "Jurisdiction" in pred.percentile or "Compliance" in pred.percentile
    assert pred.confidence_score >= 0.80
    assert len(pred.calibrated_action) > 10


def test_ml_models_api_endpoints(client):
    # GET benchmark
    bm_resp = client.get("/api/v1/ml/models/benchmark")
    assert bm_resp.status_code == 200
    bm_data = bm_resp.json()
    assert len(bm_data["models"]) == 3
    assert "XGBoost" in bm_data["champion_model"]

    # POST predict
    pred_resp = client.post(
        "/api/v1/ml/models/predict",
        json={"establishment_id": "EST-001", "worker_count": 300, "hazardous_process": False},
    )
    assert pred_resp.status_code == 200
    pred_data = pred_resp.json()
    assert pred_data["establishment_id"] == "EST-001"
    assert 10.0 <= pred_data["risk_score"] <= 100.0
    assert pred_data["priority_class"] in ["HIGH", "MEDIUM", "LOW"]
