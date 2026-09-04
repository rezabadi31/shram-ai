"""
Unit and Integration Tests for Statutory Reports & Safe Harbour Certification (Phase 28).
"""
import pytest
from app.reports.report_generator import ReportGeneratorService
from app.schemas.reports import (
    RecalibrationResponse,
    SafeHarbourCertificateSchema,
    InspectorReportDownloadSchema,
)


def test_recalibrate_compliance_logic():
    res = ReportGeneratorService.recalibrate_compliance(
        establishment_id="EST-001",
        action_ids=["ACT-001", "ACT-002"],
        remarks="Disbursed arrears to 3 contract workers and reconciled muster rolls.",
    )
    assert isinstance(res, RecalibrationResponse)
    assert res.establishment_id == "EST-001"
    assert res.cured_actions_count >= 2
    assert res.recalibrated_score > res.previous_score
    assert res.penalty_reduction_inr > 0
    assert res.safe_harbour_eligible is True or res.score_delta_to_safe_harbour >= 0


def test_safe_harbour_certificate_generation():
    # Provide score >= 85
    cert = ReportGeneratorService.generate_safe_harbour_certificate(
        establishment_id="EST-001",
        override_score=92.0,
    )
    assert isinstance(cert, SafeHarbourCertificateSchema)
    assert cert.establishment_id == "EST-001"
    assert cert.certified_compliance_score == 92.0
    assert cert.validity_days == 180
    assert cert.safe_harbour_status == "CERTIFIED_ACTIVE"
    assert len(cert.verification_hash_sha256) == 64
    assert len(cert.statutory_citations) >= 2
    assert "Office of Chief Labour Commissioner" in cert.issuing_authority


def test_safe_harbour_blocked_if_low_score():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        ReportGeneratorService.generate_safe_harbour_certificate(
            establishment_id="EST-001",
            override_score=65.0,
        )
    assert exc_info.value.status_code == 400
    assert "Minimum compliance score of 85.0 required" in exc_info.value.detail


def test_inspector_dossier_export():
    dossier = ReportGeneratorService.generate_inspector_dossier_report("EST-001")
    assert isinstance(dossier, InspectorReportDownloadSchema)
    assert dossier.establishment_id == "EST-001"
    assert dossier.composite_risk_score > 0
    assert len(dossier.top_shap_contributors) >= 2
    assert len(dossier.compliance_findings) >= 2
    assert len(dossier.cross_document_anomalies) >= 2
    assert len(dossier.recommended_inspection_focus) >= 3


def test_reports_api_endpoints(client):
    # Recalibrate
    recal_res = client.post(
        "/api/v1/reports/employer/EST-001/recalibrate",
        json={
            "action_ids": ["ACT-001", "ACT-002", "ACT-003"],
            "proof_document_names": ["Arrears_Disbursement_Slip.pdf"],
            "remarks": "Remediated all pending wage and safety findings.",
        }
    )
    assert recal_res.status_code == 200
    recal_data = recal_res.json()
    assert recal_data["recalibrated_score"] >= 85.0
    assert recal_data["safe_harbour_eligible"] is True

    # Issue Certificate
    cert_res = client.post("/api/v1/reports/employer/EST-001/safe-harbour-certificate")
    assert cert_res.status_code == 200
    cert_data = cert_res.json()
    assert "verification_hash_sha256" in cert_data
    assert cert_data["validity_days"] == 180

    # Export Dossier
    dossier_res = client.get("/api/v1/reports/inspector/EST-001/dossier-export")
    assert dossier_res.status_code == 200
    dossier_data = dossier_res.json()
    assert dossier_data["establishment_id"] == "EST-001"
    assert len(dossier_data["top_shap_contributors"]) >= 2
