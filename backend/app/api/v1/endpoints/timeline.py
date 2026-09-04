from fastapi import APIRouter
from app.schemas.timeline import EstablishmentTimeline
from app.timeline.service import TimelineService

router = APIRouter()


@router.get("/{establishment_id}/timeline", response_model=EstablishmentTimeline)
def get_establishment_timeline(establishment_id: str):
    """
    Returns the full compliance audit trail for an establishment.
    Events include: document submissions, ML risk assessments, anomaly detections,
    inspection scheduling, violation dockets, remediation proofs, and safe-harbour outcomes.
    """
    return TimelineService.get_establishment_timeline(establishment_id)
