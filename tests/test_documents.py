import io
import os


def test_upload_pdf_document_success(client):
    file_content = b"%PDF-1.4 Mock Statutory Wage Register Content For Test"
    file = io.BytesIO(file_content)

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("ABC_Wage_Register.pdf", file, "application/pdf")},
        data={"category": "Wage Register", "establishment_id": "EST-001"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "document" in data
    doc = data["document"]
    assert doc["filename"] == "ABC_Wage_Register.pdf"
    assert doc["category"] == "Wage Register"
    assert doc["status"] == "READY"
    assert len(doc["sha256_hash"]) == 64
    assert os.path.exists(doc["storage_path"])


def test_upload_unsupported_file_type(client):
    file_content = b"echo 'bad script'"
    file = io.BytesIO(file_content)

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("malicious.sh", file, "application/x-sh")},
        data={"category": "Other", "establishment_id": "EST-001"},
    )
    assert response.status_code == 400
    assert "Unsupported file extension" in response.json()["detail"]


def test_list_and_get_uploaded_document(client):
    # Upload first
    file_content = b"%PDF-1.4 Mock Attendance Register"
    file = io.BytesIO(file_content)
    upload_res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("ABC_Attendance.pdf", file, "application/pdf")},
        data={"category": "Attendance Register", "establishment_id": "EST-001"},
    )
    doc_id = upload_res.json()["document"]["id"]

    # List documents
    list_res = client.get("/api/v1/documents")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] >= 1

    # Get by ID
    get_res = client.get(f"/api/v1/documents/{doc_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == doc_id
    assert get_res.json()["category"] == "Attendance Register"


def test_download_uploaded_document(client):
    file_content = b"%PDF-1.4 Downloadable File Content 12345"
    file = io.BytesIO(file_content)
    upload_res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("Download_Test.pdf", file, "application/pdf")},
        data={"category": "Return", "establishment_id": "EST-001"},
    )
    doc_id = upload_res.json()["document"]["id"]

    download_res = client.get(f"/api/v1/documents/{doc_id}/download")
    assert download_res.status_code == 200
    assert download_res.content == file_content
