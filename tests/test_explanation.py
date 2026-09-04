from app.explanation.generator import ExplanationService
from app.schemas.explanation import (
    InspectorExplanationBrief,
    EmployerRemediationPlan,
    ComprehensiveExplanationResponse,
)


def test_inspector_explanation_generation():
    brief = ExplanationService.generate_inspector_explanation(
        establishment_id="EST-001",
        worker_count=420,
        wage_violation_count=3,
        ghost_worker_count=1,
    )
    assert isinstance(brief, InspectorExplanationBrief)
    assert brief.establishment_id == "EST-001"
    assert brief.risk_score >= 70.0
    assert brief.priority_class == "HIGH"

    # Verify statutory citations
    sections = [e.section for e in brief.statutory_exposures]
    assert any("Section 6(1)" in s for s in sections)
    assert any("Section 14" in s for s in sections)
    assert any("Section 23" in s for s in sections)

    # Verify physical evidence seizure list
    docs = " ".join(brief.mandatory_documents_to_seize).lower()
    assert "form b" in docs
    assert "utr" in docs
    assert "turnstile" in docs or "biometric" in docs

    # Verify cross-examination checklist
    checklist = " ".join(brief.cross_examination_checklist).lower()
    assert "ghost worker" in checklist or "muster roll" in checklist


def test_employer_remediation_plan_generation():
    plan = ExplanationService.generate_employer_remediation_plan(
        establishment_id="EST-001",
        worker_count=420,
        wage_violation_count=3,
        ghost_worker_count=1,
    )
    assert isinstance(plan, EmployerRemediationPlan)
    assert plan.establishment_id == "EST-001"
    assert len(plan.remediation_steps) >= 3
    assert plan.total_estimated_arrears_inr > 0

    # Verify root-causes
    roots = " ".join(plan.root_cause_analysis).lower()
    assert "minimum wage" in roots or "overtime" in roots

    # Verify safe harbour mention
    assert "14" in plan.safe_harbour_guidelines or "safe harbour" in plan.safe_harbour_guidelines.lower()


def test_comprehensive_explanation():
    comp = ExplanationService.generate_comprehensive_explanation("EST-001")
    assert isinstance(comp, ComprehensiveExplanationResponse)
    assert comp.zero_hallucination_verified is True
    assert comp.ml_risk_score == comp.inspector_brief.risk_score
    assert comp.priority_class == comp.inspector_brief.priority_class
    assert comp.establishment_name == "ABC Industries Ltd."


def test_explanation_api_endpoints(client):
    # Comprehensive generate
    res1 = client.post("/api/v1/explanation/generate", json={"establishment_id": "EST-001"})
    assert res1.status_code == 200
    d1 = res1.json()
    assert d1["zero_hallucination_verified"] is True
    assert "inspector_brief" in d1
    assert "employer_remediation" in d1

    # Inspector brief
    res2 = client.post("/api/v1/explanation/inspector-brief", json={"establishment_id": "EST-001"})
    assert res2.status_code == 200
    d2 = res2.json()
    assert "statutory_exposures" in d2
    assert len(d2["mandatory_documents_to_seize"]) >= 3

    # Employer remediation
    res3 = client.post("/api/v1/explanation/employer-remediation", json={"establishment_id": "EST-001"})
    assert res3.status_code == 200
    d3 = res3.json()
    assert "remediation_steps" in d3
    assert d3["total_estimated_arrears_inr"] > 0
