from app.timeline.service import TimelineService
from app.schemas.timeline import EstablishmentTimeline


def test_timeline_returns_events():
    timeline = TimelineService.get_establishment_timeline("EST-001")
    assert isinstance(timeline, EstablishmentTimeline)
    assert timeline.total_events >= 10
    assert len(timeline.events) == timeline.total_events
    assert timeline.establishment_id == "EST-001"


def test_timeline_event_types():
    timeline = TimelineService.get_establishment_timeline("EST-001")
    event_types = {e.event_type for e in timeline.events}
    assert "DOCUMENT_SUBMITTED" in event_types
    assert "COMPLIANCE_EVALUATED" in event_types
    assert "RISK_ASSESSED" in event_types
    assert "INSPECTION_SCHEDULED" in event_types
    assert "VIOLATION_DETECTED" in event_types
    assert "SAFE_HARBOUR_ACHIEVED" in event_types


def test_timeline_severity_values():
    timeline = TimelineService.get_establishment_timeline("EST-001")
    valid = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
    for ev in timeline.events:
        assert ev.severity in valid
        assert ev.actor_type in {"EMPLOYER", "INSPECTOR", "SYSTEM", "ML_ENGINE"}


def test_timeline_api_endpoint(client):
    res = client.get("/api/v1/establishments/EST-001/timeline")
    assert res.status_code == 200
    data = res.json()
    assert data["total_events"] >= 10
    assert len(data["events"]) == data["total_events"]

    # Verify first and last event dates present
    assert data["first_audit_date"]
    assert data["last_activity_date"]

    # Verify all events have required fields
    for ev in data["events"]:
        assert ev["event_id"].startswith("EVT-")
        assert ev["event_type"]
        assert ev["title"]
        assert ev["description"]
