from app.ml.feature_extractor import RiskFeatureExtractor
from app.schemas.features import FeatureCategory


def test_feature_definitions_registry():
    defs = RiskFeatureExtractor.get_feature_definitions()
    assert len(defs) == 22

    # Check categories
    categories = {d.category for d in defs}
    assert categories == {
        FeatureCategory.DEMOGRAPHIC,
        FeatureCategory.DETERMINISTIC,
        FeatureCategory.ANOMALY,
        FeatureCategory.HISTORICAL,
        FeatureCategory.INTERACTION,
    }

    # Check names are unique
    names = [d.name for d in defs]
    assert len(names) == len(set(names))


def test_extract_single_establishment_features():
    res = RiskFeatureExtractor.extract_features(
        establishment_id="EST-001",
        worker_count=420,
        contract_worker_ratio=0.45,
        hazardous_process=True,
        wage_violation_count=3,
        ghost_worker_count=1,
    )
    assert res.establishment_id == "EST-001"
    assert res.feature_count == 22
    assert len(res.features) == 22
    assert len(res.vector) == 22

    # Verify normalized bounds
    for item in res.features:
        assert 0.0 <= item.normalized_value <= 1.0
        assert len(item.formula) > 0


def test_extract_matrix_and_summary():
    X, y, feature_names = RiskFeatureExtractor.extract_matrix_from_dataset()
    assert len(X) >= 100
    assert len(y) == len(X)
    assert len(feature_names) == 22
    assert len(X[0]) == 22

    # Check summary
    summary = RiskFeatureExtractor.compute_matrix_summary()
    assert summary.feature_count == 22
    assert summary.sample_count >= 100
    assert len(summary.features) == 22

    for f in summary.features:
        assert f.std >= 0.0
        assert f.min_val <= f.mean <= f.max_val


def test_feature_engineering_api_endpoints(client):
    # GET definitions
    def_resp = client.get("/api/v1/ml/features/definitions")
    assert def_resp.status_code == 200
    defs = def_resp.json()
    assert len(defs) == 22

    # POST extract
    ext_resp = client.post(
        "/api/v1/ml/features/extract",
        json={"establishment_id": "EST-001", "worker_count": 250, "hazardous_process": True},
    )
    assert ext_resp.status_code == 200
    ext_data = ext_resp.json()
    assert ext_data["feature_count"] == 22
    assert len(ext_data["features"]) == 22

    # GET matrix-summary
    mat_resp = client.get("/api/v1/ml/features/matrix-summary")
    assert mat_resp.status_code == 200
    mat_data = mat_resp.json()
    assert mat_data["feature_count"] == 22
    assert mat_data["sample_count"] >= 100
