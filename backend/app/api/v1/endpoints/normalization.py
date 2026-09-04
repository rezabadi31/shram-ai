from fastapi import APIRouter, HTTPException, status
from app.schemas.normalization import NormalizedDocumentDossier
from app.document_ai.normalizer import DataNormalizerService

router = APIRouter()


@router.post(
    "/{document_id}/normalize",
    response_model=NormalizedDocumentDossier,
    tags=["Data Normalization"],
)
async def normalize_document_data(document_id: str):
    """
    Normalizes varied document tables into canonical statutory schemas
    (EmployeeRecord, WageRecord, AttendanceRecord, PayrollRecord) and calculates data quality scores.
    """
    try:
        return DataNormalizerService.normalize_document(document_id)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Normalization failed: {str(e)}",
        )


@router.get(
    "/{document_id}/normalized",
    response_model=NormalizedDocumentDossier,
    tags=["Data Normalization"],
)
async def get_normalized_document_data(document_id: str):
    """
    Retrieves canonical records, quality scores, and missing field alerts for a document.
    """
    try:
        return DataNormalizerService.normalize_document(document_id)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
