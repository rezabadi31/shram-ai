import io
from PIL import Image


def test_ocr_fallback_pipeline_for_image(client):
    # Create test image in memory
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # 1. Upload test scanned image
    upload_res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("Scanned_Muster_Roll.png", img_bytes, "image/png")},
        data={"category": "Attendance Register", "establishment_id": "EST-001"},
    )
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["document"]["id"]

    # 2. Trigger Extraction Pipeline
    extract_res = client.post(f"/api/v1/documents/{doc_id}/extract")
    assert extract_res.status_code == 200
    data = extract_res.json()

    assert data["document_id"] == doc_id
    assert data["extraction_method"] == "OCR_FALLBACK"
    assert data["overall_confidence"] > 0.8
    assert len(data["tables"]) >= 1

    first_table = data["tables"][0]
    assert first_table["row_count"] >= 1
    first_row = first_table["rows"][0]
    assert "provenance" in first_row
    assert first_row["provenance"]["document_id"] == doc_id
    assert first_row["provenance"]["page"] == 1


def test_pdf_extraction_pipeline(client):
    file_content = b"%PDF-1.4 Mock Statutory Wage Register Document Stream"
    file = io.BytesIO(file_content)

    upload_res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("Wage_Register_Nov2024.pdf", file, "application/pdf")},
        data={"category": "Wage Register", "establishment_id": "EST-001"},
    )
    doc_id = upload_res.json()["document"]["id"]

    get_extract_res = client.get(f"/api/v1/documents/{doc_id}/extraction")
    assert get_extract_res.status_code == 200
    data = get_extract_res.json()
    assert data["document_id"] == doc_id
    assert len(data["tables"]) >= 1
    assert data["extracted_records_count"] >= 1


def test_extract_nonexistent_document(client):
    res = client.post("/api/v1/documents/DOC-NONEXISTENT/extract")
    assert res.status_code == 404
