from fastapi.testclient import TestClient
from app.main import app
from app.analytics.service import AnalyticsService

client = TestClient(app)


def test_get_macro_overview():
    overview = AnalyticsService.get_macro_overview()
    assert overview is not None
    assert overview.national_compliance_index >= 70.0
    assert overview.total_registered_workforce > 1000000
    assert overview.total_active_establishments > 5000
    assert overview.total_arrears_recovered_inr > 0
    assert len(overview.jurisdictions) >= 5
    assert len(overview.sectors) >= 5
    assert len(overview.monthly_trend) >= 8


def test_jurisdiction_metrics():
    jurisdictions = AnalyticsService.get_jurisdictions()
    assert len(jurisdictions) == 5
    ids = [j.jurisdiction_id for j in jurisdictions]
    assert "JUR-PUN-01" in ids
    assert "JUR-MUM-02" in ids
    assert "JUR-THA-03" in ids

    for j in jurisdictions:
        assert j.sphere == "CENTRAL"
        assert j.total_establishments > j.high_risk_count
        assert 0 <= j.compliance_rate_pct <= 100
        assert j.arrears_recovered_inr > 0


def test_sector_risk_metrics():
    sectors = AnalyticsService.get_sectors()
    assert len(sectors) >= 5
    for s in sectors:
        assert s.hazard_tier in {"HIGH_HAZARD", "MEDIUM_HAZARD", "LOW_HAZARD"}
        assert s.non_compliance_rate_pct > 0
        assert s.top_violation_code != ""
        assert s.estimated_underpayment_inr > 0


def test_monthly_trend_points():
    trend = AnalyticsService.get_monthly_trend()
    assert len(trend) >= 8
    # Assert compliance index increases over time as automated audits & safe harbour take effect
    assert trend[-1].compliance_index > trend[0].compliance_index
    assert trend[-1].safe_harbour_achieved > trend[0].safe_harbour_achieved


def test_analytics_api_endpoints():
    # 1. Test GET /api/v1/analytics/macro-overview
    res1 = client.get("/api/v1/analytics/macro-overview")
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["national_compliance_index"] > 75.0
    assert len(data1["jurisdictions"]) == 5

    # 2. Test GET /api/v1/analytics/jurisdictions
    res2 = client.get("/api/v1/analytics/jurisdictions")
    assert res2.status_code == 200
    data2 = res2.json()
    assert isinstance(data2, list)
    assert len(data2) == 5

    # 3. Test GET /api/v1/analytics/sector-risk-matrix
    res3 = client.get("/api/v1/analytics/sector-risk-matrix")
    assert res3.status_code == 200
    data3 = res3.json()
    assert isinstance(data3, list)
    assert any(s["hazard_tier"] == "HIGH_HAZARD" for s in data3)
