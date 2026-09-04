"""
Statutory Reports and Safe Harbour Certification API Endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.reports import (
    CureActionRequest,
    RecalibrationResponse,
    SafeHarbourCertificateSchema,
    InspectorReportDownloadSchema,
)
from app.schemas.auth import UserResponse, RoleEnum
from app.reports.report_generator import ReportGeneratorService
from app.api.deps import (
    get_current_user_optional,
    verify_establishment_ownership,
)

router = APIRouter()


def ensure_inspector_access(user: Optional[UserResponse]):
    if user and user.role not in (RoleEnum.INSPECTOR, RoleEnum.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Restricted — Your account does not have Inspector permissions.",
        )


@router.post("/employer/{establishment_id}/recalibrate", response_model=RecalibrationResponse)
def recalibrate_employer_compliance(
    establishment_id: str,
    req: CureActionRequest,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Submits cured non-compliance actions and recalibrates the establishment's
    voluntary compliance score in real time.
    """
    if current_user:
        if current_user.role != RoleEnum.EMPLOYER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Restricted — This portal is designated exclusively for registered Employers.",
            )
        verify_establishment_ownership(establishment_id, current_user)

    return ReportGeneratorService.recalibrate_compliance(
        establishment_id=establishment_id,
        action_ids=req.action_ids,
        remarks=req.remarks,
    )


@router.post("/employer/{establishment_id}/safe-harbour-certificate", response_model=SafeHarbourCertificateSchema)
def issue_safe_harbour_certificate(
    establishment_id: str,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Generates and issues a cryptographically verified Safe Harbour Compliance Certificate (Form SH-01).
    Requires compliance score >= 85.0.
    """
    if current_user:
        if current_user.role != RoleEnum.EMPLOYER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Restricted — This portal is designated exclusively for registered Employers.",
            )
        verify_establishment_ownership(establishment_id, current_user)

    return ReportGeneratorService.generate_safe_harbour_certificate(establishment_id)


@router.get("/inspector/{establishment_id}/dossier-export", response_model=InspectorReportDownloadSchema)
def export_inspector_dossier_report(
    establishment_id: str,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Exports the complete Inspector Intelligence Dossier report for an establishment.
    """
    ensure_inspector_access(current_user)
    return ReportGeneratorService.generate_inspector_dossier_report(establishment_id)
