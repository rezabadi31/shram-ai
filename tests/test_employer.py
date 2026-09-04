from app.employer.service import EmployerService
from app.schemas.employer import EmployerComplianceProfile, PenaltyExposureItem


def test_employer_compliance_profile():
    profile = EmployerService.get_compliance_profile("EST-001")
    assert isinstance(profile, EmployerComplianceProfile)
    assert profile.establishment_id == "EST-001"
    assert profile.ml_risk_score > 0
    assert profile.voluntary_compliance_score > 0
    assert profile.voluntary_compliance_score <= 100
    assert profile.total_penalty_exposure_inr > 0
    assert len(profile.register_statuses) >= 3
    assert len(profile.corrective_actions) >= 2
    assert len(profile.penalty_exposures) >= 2
    assert profile.priority_class in ("HIGH", "MEDIUM", "LOW")


def test_penalty_exposure_breakdown():
    profile = EmployerService.get_compliance_profile("EST-001")
    applicable = [p for p in profile.penalty_exposures if p.applicable]
    assert len(applicable) >= 2
    for p in applicable:
        assert p.maximum_fine_inr > 0
        assert p.section
        assert p.code_name

    total = sum(p.maximum_fine_inr for p in applicable)
    assert profile.total_penalty_exposure_inr == total


def test_employer_safe_harbour_delta():
    profile = EmployerService.get_compliance_profile("EST-001")
    # delta should be non-negative (score below 85 safe harbour)
    assert profile.score_delta_to_safe_harbour >= 0


def test_employer_api_endpoints(client):
    # GET profile
    res = client.get("/api/v1/employer/EST-001/profile")
    assert res.status_code == 200
    data = res.json()
    assert "ml_risk_score" in data
    assert "total_penalty_exposure_inr" in data
    assert data["total_penalty_exposure_inr"] > 0
    assert len(data["register_statuses"]) >= 3
    assert len(data["corrective_actions"]) >= 2

    # GET penalty-exposure
    res2 = client.get("/api/v1/employer/EST-001/penalty-exposure")
    assert res2.status_code == 200
    items = res2.json()
    assert len(items) >= 2
    applicable = [i for i in items if i["applicable"]]
    assert len(applicable) >= 2
