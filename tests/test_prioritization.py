from app.prioritization.queue_manager import InspectionQueueManager
from app.schemas.prioritization import (
    PrioritizationFilterParams,
    InspectionScheduleBatchRequest,
)


def test_prioritized_queue_retrieval():
    queue = InspectionQueueManager.get_prioritized_queue(
        PrioritizationFilterParams(page=1, page_size=25)
    )
    assert queue.total_count >= 100
    assert len(queue.items) == 25

    # Check ordering
    for i in range(len(queue.items) - 1):
        assert queue.items[i].composite_priority_score >= queue.items[i + 1].composite_priority_score


def test_randomized_audit_quota():
    queue = InspectionQueueManager.get_prioritized_queue(
        PrioritizationFilterParams(page=1, page_size=200)
    )
    reasons = [item.selection_reason for item in queue.items]
    assert "RANDOM_AUDIT_CONTROL" in reasons
    assert "RISK_DRIVEN" in reasons

    random_controls = [i for i in queue.items if i.selection_reason == "RANDOM_AUDIT_CONTROL"]
    assert len(random_controls) >= 5
    for rc in random_controls:
        assert rc.composite_priority_score >= 70.0  # boosted for scheduling visibility


def test_batch_scheduling():
    queue = InspectionQueueManager.get_prioritized_queue(
        PrioritizationFilterParams(page=1, page_size=5)
    )
    target_ids = [queue.items[0].establishment_id, queue.items[1].establishment_id]

    res = InspectionQueueManager.schedule_inspection_batch(
        InspectionScheduleBatchRequest(
            establishment_ids=target_ids,
            inspector_id="INS-OFFICER-TEST",
            urgency="IMMEDIATE_72H",
        )
    )
    assert res.scheduled_count == 2
    assert res.inspector_id == "INS-OFFICER-TEST"
    assert "72 Hours" in res.target_window

    for item in res.scheduled_items:
        assert item.inspection_status == "SCHEDULED"
        assert item.assigned_inspector_id == "INS-OFFICER-TEST"


def test_prioritization_api_endpoints(client):
    # POST queue
    q_resp = client.post(
        "/api/v1/prioritization/queue",
        json={"page": 1, "page_size": 15, "priority_class": "HIGH"},
    )
    assert q_resp.status_code == 200
    q_data = q_resp.json()
    assert "total_count" in q_data
    assert len(q_data["items"]) <= 15
    for item in q_data["items"]:
        assert item["priority_class"] == "HIGH"

    # POST schedule
    sched_resp = client.post(
        "/api/v1/prioritization/schedule",
        json={"establishment_ids": ["EST-001"], "inspector_id": "INS-API-01"},
    )
    assert sched_resp.status_code == 200
    sched_data = sched_resp.json()
    assert sched_data["scheduled_count"] == 1

    # GET metrics
    m_resp = client.get("/api/v1/prioritization/metrics")
    assert m_resp.status_code == 200
    m_data = m_resp.json()
    assert "monthly_inspector_capacity" in m_data
    assert m_data["high_priority_count"] >= 1
