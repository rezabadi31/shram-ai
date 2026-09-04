import os
from fastapi import APIRouter, HTTPException, status
from app.schemas.classification import ClassificationResult, TextClassificationRequest
from app.document_ai.document_classifier import DocumentClassifierService
from app.document_ai.upload import UploadService
from app.document_ai.pipeline import DocumentIntelligencePipeline

router = APIRouter()


@router.post(
    "/classify-text",
    response_model=ClassificationResult,
    tags=["Document Classification"],
)
async def classify_text(request: TextClassificationRequest):
    """
    Classifies raw text or OCR output using deterministic rules and ML TF-IDF fallback.
    """
    return DocumentClassifierService.classify(
        text=request.text,
        filename=request.filename,
    )


@router.post(
    "/{document_id}/classify",
    response_model=ClassificationResult,
    tags=["Document Classification"],
)
async def classify_document(document_id: str):
    """
    Automatically classifies an uploaded statutory register based on its filename and extracted text.
    """
    doc = UploadService.get_document(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' not found",
        )

    # Obtain extracted text or fallback
    extracted = DocumentIntelligencePipeline.get_cached_result(document_id)
    text_content = extracted.raw_text_sample if extracted else doc.filename

    result = DocumentClassifierService.classify(
        text=text_content,
        filename=doc.filename,
    )
    result.document_id = document_id
    return result
