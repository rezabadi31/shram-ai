from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from app.schemas.inspection import (
    InspectionSession,
    InspectionSessionSubmitRequest,
    InspectionSessionResponse,
)
from app.schemas.auth import UserResponse, RoleEnum
from app.inspection.service import InspectionService
from app.api.deps import get_current_user_optional

router = APIRouter()


def check_inspector_access(user: Optional[UserResponse]):
    if user and user.role not in (RoleEnum.INSPECTOR, RoleEnum.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Restricted — Your account does not have Inspector permissions.",
        )


@router.post("/start", response_model=InspectionSession)
def start_inspection_session(
    establishment_id: str,
    establishment_name: str,
    inspector_id: str = "INS-OFFICER-42",
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Creates and returns a new stateful inspection session with the standard
    10-item statutory checklist (Wage Registers, Attendance, Safety, Social Security).
    """
    check_inspector_access(current_user)
    return InspectionService.create_session(establishment_id, establishment_name, inspector_id)


@router.get("/{session_id}", response_model=InspectionSession)
def get_inspection_session(
    session_id: str,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """Retrieves an active inspection session by ID."""
    check_inspector_access(current_user)
    session = InspectionService.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    return session


@router.post("/submit", response_model=InspectionSessionResponse)
def submit_inspection_session(
    req: InspectionSessionSubmitRequest,
    current_user: Optional[UserResponse] = Depends(get_current_user_optional),
):
    """
    Submits a completed inspection session. Generates a violation docket
    with per-section penalty proposals and returns a report reference.
    """
    check_inspector_access(current_user)
    return InspectionService.submit_session(req)

