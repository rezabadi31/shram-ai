import os
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from app.schemas.document import (
    DocumentCategory,
    DocumentMetadata,
    DocumentUploadResponse,
    DocumentListResponse,
)
from app.document_ai.upload import UploadService

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"],
)
async def upload_document(
    file: UploadFile = File(...),
    category: DocumentCategory = Form(DocumentCategory.WAGE_REGISTER),
    establishment_id: str = Form("EST-001"),
):
    """
    Upload and ingest a statutory labour document (PDF, scanned PDF, PNG, JPG).
    Validates mime-type, computes SHA-256 checksum, stores to disk, and transitions lifecycle.
    """
    metadata = await UploadService.process_and_store_upload(
        file=file,
        category=category,
        establishment_id=establishment_id,
    )
    return DocumentUploadResponse(
        message="Document uploaded, checksummed, and queued for processing successfully",
        document=metadata,
    )


@router.get("", response_model=DocumentListResponse, tags=["Documents"])
async def list_documents(establishment_id: Optional[str] = None):
    """List all uploaded statutory registers, optionally filtered by establishment."""
    docs = UploadService.list_documents(establishment_id=establishment_id)
    return DocumentListResponse(total=len(docs), documents=docs)


@router.get("/{document_id}", response_model=DocumentMetadata, tags=["Documents"])
async def get_document_metadata(document_id: str):
    """Retrieve metadata, SHA-256 checksum, and audit status of an uploaded document."""
    doc = UploadService.get_document(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' not found",
        )
    return doc


@router.get("/{document_id}/download", tags=["Documents"])
async def download_document(document_id: str):
    """Download or view the raw statutory document file."""
    doc = UploadService.get_document(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' not found",
        )
    if not os.path.exists(doc.storage_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File content not found on storage disk",
        )
    return FileResponse(
        path=doc.storage_path,
        filename=doc.filename,
        media_type=doc.content_type,
    )
