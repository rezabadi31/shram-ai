from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.notice import (
    StatutoryNotice,
    GenerateNoticeRequest,
    UpdateNoticeStatusRequest,
)
from app.notices.service import NoticeService

router = APIRouter()


@router.post("/generate", response_model=StatutoryNotice)
def generate_statutory_notice(req: GenerateNoticeRequest):
    """
    Generate an official statutory show cause or rectification notice with formal
    citations, penalty exposures, and SHA-256 digital signature seal.
    """
    return NoticeService.generate_notice(req)


@router.get("/{notice_id}", response_model=StatutoryNotice)
def get_notice(notice_id: str):
    """
    Retrieve a statutory notice by its unique identifier.
    """
    notice = NoticeService.get_notice(notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail=f"Notice '{notice_id}' not found.")
    return notice


@router.get("/establishment/{establishment_id}", response_model=List[StatutoryNotice])
def list_establishment_notices(establishment_id: str):
    """
    List all statutory notices issued to a given establishment.
    """
    return NoticeService.list_establishment_notices(establishment_id)


@router.post("/{notice_id}/status", response_model=StatutoryNotice)
def update_notice_status(notice_id: str, req: UpdateNoticeStatusRequest):
    """
    Update the status of a statutory notice (e.g. RESPONDED, COMPOUNDED, CLOSED).
    """
    updated = NoticeService.update_notice_status(notice_id, req.status, req.response_notes)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Notice '{notice_id}' not found.")
    return updated
