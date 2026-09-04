from fastapi.testclient import TestClient
from app.main import app
from app.notices.service import NoticeService
from app.schemas.notice import GenerateNoticeRequest, UpdateNoticeStatusRequest

client = TestClient(app)


def test_get_default_notice():
    notice = NoticeService.get_notice("NOT-2024-001")
    assert notice is not None
    assert notice.establishment_id == "EST-001"
    assert notice.notice_type == "SHOW_CAUSE"
    assert notice.total_penalty_exposure_inr > 0
    assert len(notice.violations) >= 3
    assert notice.digital_signature_hash.startswith("SHA256:")
    assert "GOVERNMENT OF INDIA" in notice.formal_legal_text


def test_generate_statutory_notice():
    req = GenerateNoticeRequest(
        establishment_id="EST-002",
        notice_type="SHOW_CAUSE",
        issuing_officer="INS-OFFICER-42",
        custom_instructions="Verify overtime payments under Section 13.",
    )
    notice = NoticeService.generate_notice(req)
    assert notice.notice_id.startswith("NOT-")
    assert notice.establishment_id == "EST-002"
    assert notice.status == "ISSUED"
    assert notice.issuing_officer == "INS-OFFICER-42"
    assert notice.digital_signature_hash.startswith("SHA256:")
    assert len(notice.violations) > 0


def test_list_establishment_notices():
    notices = NoticeService.list_establishment_notices("EST-001")
    assert isinstance(notices, list)
    assert len(notices) >= 1
    assert any(n.notice_id == "NOT-2024-001" for n in notices)


def test_update_notice_status():
    updated = NoticeService.update_notice_status(
        "NOT-2024-001",
        "RESPONDED",
        "Employer submitted RTGS payment scroll confirming compliance."
    )
    assert updated is not None
    assert updated.status == "RESPONDED"
    assert updated.metadata.get("response_notes") is not None


def test_notices_api_endpoints():
    # 1. Get establishment notices
    res1 = client.get("/api/v1/notices/establishment/EST-001")
    assert res1.status_code == 200
    data1 = res1.json()
    assert isinstance(data1, list)
    assert len(data1) >= 1

    # 2. Get specific notice
    res2 = client.get("/api/v1/notices/NOT-2024-001")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["notice_id"] == "NOT-2024-001"
    assert "SHA256:" in data2["digital_signature_hash"]

    # 3. Generate notice via API
    res3 = client.post(
        "/api/v1/notices/generate",
        json={
            "establishment_id": "EST-001",
            "notice_type": "SHOW_CAUSE",
            "issuing_officer": "INS-OFFICER-37 (Central Sphere)",
        },
    )
    assert res3.status_code == 200
    data3 = res3.json()
    assert data3["status"] == "ISSUED"
    new_notice_id = data3["notice_id"]

    # 4. Update status via API
    res4 = client.post(
        f"/api/v1/notices/{new_notice_id}/status",
        json={"status": "CLOSED", "response_notes": "All arrears settled."},
    )
    assert res4.status_code == 200
    data4 = res4.json()
    assert data4["status"] == "CLOSED"
