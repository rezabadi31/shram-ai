from app.inspection.service import InspectionService
from app.schemas.inspection import InspectionSession, InspectionSessionResponse, InspectionChecklistItem, InspectionSessionSubmitRequest


def test_create_inspection_session():
    session = InspectionService.create_session("EST-001", "ABC Industries Ltd.", "INS-42")
    assert isinstance(session, InspectionSession)
    assert session.status == "ACTIVE"
    assert len(session.checklist) == 10
    assert session.violations_found == 0
    assert session.total_penalty_proposed_inr == 0.0
    assert session.session_id.startswith("INSP-")


def test_checklist_categories():
    session = InspectionService.create_session("EST-001", "ABC Industries Ltd.", "INS-42")
    categories = {item.category for item in session.checklist}
    assert "Wage Registers" in categories
    assert "Attendance Records" in categories
    assert "Safety Compliance" in categories
    assert "Social Security" in categories


def test_submit_session_generates_docket():
    session = InspectionService.create_session("EST-002", "Bharat Garments", "INS-43")

    # Simulate 2 violations found during inspection
    updated_checklist = list(session.checklist)
    updated_checklist[0] = InspectionChecklistItem(
        **{**updated_checklist[0].model_dump(),
           "is_verified": True,
           "severity": "CRITICAL",
           "finding": "Form B entries show ₹340 shortfall against minimum wage floor for 3 unskilled workers"}
    )
    updated_checklist[5] = InspectionChecklistItem(
        **{**updated_checklist[5].model_dump(),
           "is_verified": True,
           "severity": "HIGH",
           "finding": "Safety Committee not constituted — no display board found on factory floor"}
    )

    req = InspectionSessionSubmitRequest(
        session_id=session.session_id,
        establishment_id="EST-002",
        inspector_id="INS-43",
        checklist=updated_checklist,
        documents_seized=["Form B (Oct 2024)", "Attendance Muster Roll Oct 2024"],
        field_notes="Worker interviews corroborate underpayment claims. Form B register available but shows incorrect rates.",
    )

    result = InspectionService.submit_session(req)
    assert isinstance(result, InspectionSessionResponse)
    assert result.status == "SUBMITTED"
    assert result.violations_found == 2
    assert result.total_penalty_proposed_inr >= 70000.0  # 50K + 20K
    assert len(result.violation_docket) == 2
    assert result.report_ref.startswith("RPT-")


def test_inspection_api_endpoints(client):
    # Start session
    res = client.post(
        "/api/v1/inspection/start",
        params={"establishment_id": "EST-001", "establishment_name": "ABC Industries Ltd.", "inspector_id": "INS-42"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ACTIVE"
    assert len(data["checklist"]) == 10
    session_id = data["session_id"]

    # Retrieve session
    res2 = client.get(f"/api/v1/inspection/{session_id}")
    assert res2.status_code == 200

    # Submit session
    checklist = data["checklist"]
    checklist[0]["severity"] = "CRITICAL"
    checklist[0]["is_verified"] = True
    checklist[0]["finding"] = "Wage below minimum floor"

    submit_res = client.post("/api/v1/inspection/submit", json={
        "session_id": session_id,
        "establishment_id": "EST-001",
        "inspector_id": "INS-42",
        "checklist": checklist,
        "documents_seized": ["Form B Register"],
        "field_notes": "Confirmed wage underpayment."
    })
    assert submit_res.status_code == 200
    submit_data = submit_res.json()
    assert submit_data["status"] == "SUBMITTED"
    assert submit_data["violations_found"] >= 1
