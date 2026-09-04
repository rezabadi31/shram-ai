import io
from app.document_ai.normalizer import DataNormalizerService


def test_currency_parser():
    assert DataNormalizerService.parse_currency("₹ 16,200.00") == 16200.0
    assert DataNormalizerService.parse_currency("16200/-") == 16200.0
    assert DataNormalizerService.parse_currency("550.50") == 550.5
    assert DataNormalizerService.parse_currency(None) == 0.0
    assert DataNormalizerService.parse_currency(12500) == 12500.0


def test_column_alias_matching():
    row = {"token_no": "EMP-99", "rate_per_day": "650", "take_home": "16900"}
    assert DataNormalizerService.match_column("employee_id", row) == "EMP-99"
    assert DataNormalizerService.match_column("daily_wage_rate", row) == "650"
    assert DataNormalizerService.match_column("net_payable", row) == "16900"


def test_normalize_wage_document(client):
    file_content = b"%PDF-1.4 Mock Wage Register\nSl | Emp ID | Employee Name | Wage Rate | Days Worked | Deductions | Net Paid\n1 | EMP-001 | Ramesh Kumar | 650.00 | 26 | 1500.00 | 16200.00"
    file = io.BytesIO(file_content)

    upload_res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("Wage_Register_Oct2024.pdf", file, "application/pdf")},
        data={"category": "Wage Register", "establishment_id": "EST-001"},
    )
    doc_id = upload_res.json()["document"]["id"]

    norm_res = client.post(f"/api/v1/documents/{doc_id}/normalize")
    assert norm_res.status_code == 200
    data = norm_res.json()

    assert data["document_id"] == doc_id
    assert data["record_type"] == "WAGE_RECORD"
    assert data["records_count"] >= 1
    assert data["data_quality_score"] >= 0.80

    first_record = data["records"][0]
    assert "employee_id" in first_record
    assert "daily_wage_rate" in first_record
    assert "net_payable" in first_record
    assert first_record["daily_wage_rate"] > 0


def test_normalize_attendance_document(client):
    file_content = b"%PDF-1.4 Mock Muster Roll\nSl | Token | Name | Days Worked\n1 | EMP-101 | Sunita Devi | 24"
    file = io.BytesIO(file_content)

    upload_res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("Muster_Roll_Oct.pdf", file, "application/pdf")},
        data={"category": "Attendance Register", "establishment_id": "EST-001"},
    )
    doc_id = upload_res.json()["document"]["id"]

    get_norm_res = client.get(f"/api/v1/documents/{doc_id}/normalized")
    assert get_norm_res.status_code == 200
    data = get_norm_res.json()

    assert data["record_type"] == "ATTENDANCE_RECORD"
    assert data["records_count"] >= 1
    first_record = data["records"][0]
    assert first_record["days_present"] > 0
