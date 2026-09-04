from fastapi import APIRouter, HTTPException, status
from app.schemas.extraction import DocumentIntelligenceResult
from app.document_ai.pipeline import DocumentIntelligencePipeline
from app.document_ai.upload import UploadService

router = APIRouter()


@router.post(
    "/{document_id}/extract",
    response_model=DocumentIntelligenceResult,
    tags=["Document Intelligence"],
)
async def extract_document_data(document_id: str):
    """
    Triggers the Document Intelligence Pipeline:
    Direct Text Extraction -> Quality Check -> OCR Fallback -> Table Extraction -> Structured JSON.
    """
    try:
        result = DocumentIntelligencePipeline.process_document(document_id)
        return result
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction pipeline failed: {str(e)}",
        )


@router.get(
    "/{document_id}/extraction",
    response_model=DocumentIntelligenceResult,
    tags=["Document Intelligence"],
)
async def get_extraction_result(document_id: str):
    """
    Retrieve structured table extraction and OCR provenance for a processed statutory document.
    """
    cached = DocumentIntelligencePipeline.get_cached_result(document_id)
    if cached:
        return cached

    # If not yet extracted, trigger extraction on demand
    try:
        return DocumentIntelligencePipeline.process_document(document_id)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
