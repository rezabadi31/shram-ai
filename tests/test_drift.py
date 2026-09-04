from fastapi.testclient import TestClient
from app.main import app
from app.ml.drift_monitor import DriftMonitorService, _compute_psi
from app.schemas.drift import RetrainTriggerRequest
import numpy as np

client = TestClient(app)


def test_compute_psi_synthetic():
    base = np.random.normal(10, 2, 100)
    curr = np.random.normal(10, 2, 100)
    psi = _compute_psi(base, curr)
    assert isinstance(psi, float)
    assert psi >= 0.0


def test_get_drift_report():
    report = DriftMonitorService.get_drift_report()
    assert report is not None
    assert report.model_version.startswith("XGBoost")
    assert report.overall_psi >= 0.0
    assert report.drift_alert_level in {"GREEN", "YELLOW", "RED"}
    assert len(report.feature_drifts) >= 10
    assert report.inspections_ingested_count >= 1
    assert report.inspector_override_rate >= 0.0


def test_feature_drift_metric_attributes():
    report = DriftMonitorService.get_drift_report()
    feature_names = [f.feature_name for f in report.feature_drifts]
    assert "wage_violation_count" in feature_names
    assert "ghost_worker_count" in feature_names
    assert "missing_form_b_count" in feature_names

    for f in report.feature_drifts:
        assert f.psi_score >= 0.0
        assert f.drift_status in {"NO_DRIFT", "MODERATE_DRIFT", "SIGNIFICANT_DRIFT"}
        assert f.baseline_mean > 0 or f.current_mean >= 0


def test_record_inspector_feedback():
    initial_count = len(DriftMonitorService._feedback_records)
    DriftMonitorService.record_inspector_feedback("EST-004", overrides=1, total_items=7, decision="MODIFIED")
    assert len(DriftMonitorService._feedback_records) == initial_count + 1


def test_trigger_closed_loop_retraining():
    req = RetrainTriggerRequest(
        trigger_reason="DRIFT_TEST_CALIBRATION",
        include_inspector_feedback=True,
        challenger_algorithm="xgboost",
    )
    res = DriftMonitorService.trigger_closed_loop_retraining(req)
    assert res.status == "COMPLETED_SUCCESS"
    assert res.challenger_auc >= res.champion_auc
    assert res.samples_used >= 1000
    assert "XGBoost" in res.deployed_model


def test_drift_api_endpoints():
    # 1. Test GET /api/v1/ml/drift/report
    res1 = client.get("/api/v1/ml/drift/report")
    assert res1.status_code == 200
    data1 = res1.json()
    assert "overall_psi" in data1
    assert "drift_alert_level" in data1
    assert len(data1["feature_drifts"]) >= 10

    # 2. Test POST /api/v1/ml/drift/retrain
    res2 = client.post(
        "/api/v1/ml/drift/retrain",
        json={"trigger_reason": "API_TEST", "include_inspector_feedback": True},
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["status"] == "COMPLETED_SUCCESS"
    assert data2["challenger_auc"] > 0.90
