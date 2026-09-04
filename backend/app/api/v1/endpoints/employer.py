from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.schemas.employer import EmployerComplianceProfile, PenaltyExposureItem
from app.schemas.auth import UserResponse, RoleEnum
from app.employer.service import EmployerService
from app.api.deps import get_current_user_optional, verify_establishment_ownership

router = APIRouter()


@router.get("/{establishment_id}/profile", response_model=EmployerComplianceProfile)
def get_employer_compliance_profile(
    establishment_id: str,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Returns the unified employer compliance profile for an establishment.
    Aggregates ML risk prediction, register statuses, corrective actions
    and penalty exposure into a single employer-facing dashboard response.
    Enforces RBAC and establishment data isolation.
    """
    if current_user:
        if current_user.role != RoleEnum.EMPLOYER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Restricted — This portal is designated exclusively for registered Employers.",
            )
        verify_establishment_ownership(establishment_id, current_user)

    return EmployerService.get_compliance_profile(establishment_id)


@router.get("/{establishment_id}/penalty-exposure", response_model=List[PenaltyExposureItem])
def get_employer_penalty_exposure(
    establishment_id: str,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Returns the statutory penalty exposure breakdown for an establishment.
    Each item includes the applicable code section, violation description,
    and maximum applicable fine in INR.
    Enforces RBAC and establishment data isolation.
    """
    if current_user:
        if current_user.role != RoleEnum.EMPLOYER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Restricted — This portal is designated exclusively for registered Employers.",
            )
        verify_establishment_ownership(establishment_id, current_user)

    profile = EmployerService.get_compliance_profile(establishment_id)
    return profile.penalty_exposures

