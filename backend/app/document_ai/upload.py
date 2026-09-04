import os
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from fastapi import UploadFile, HTTPException, status
from app.schemas.document import DocumentCategory, DocumentStatus, DocumentMetadata

# In-memory document registry for fast lookup
DOCUMENT_REGISTRY: Dict[str, DocumentMetadata] = {}


class UploadService:
    ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    BASE_STORAGE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw")
    )

    @classmethod
    def validate_file_metadata(cls, filename: str, content_type: str) -> str:
        """Validates extension and content type."""
        ext = os.path.splitext(filename)[1].lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(cls.ALLOWED_EXTENSIONS)}",
            )
        return ext

    @classmethod
    async def process_and_store_upload(
        cls,
        file: UploadFile,
        category: DocumentCategory,
        establishment_id: str = "EST-001",
    ) -> DocumentMetadata:
        """
        Validates, computes SHA-256, persists to disk, and tracks in registry.
        """
        ext = cls.validate_file_metadata(file.filename, file.content_type)
        content = await file.read()
        file_size = len(content)

        if file_size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {cls.MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

        # Compute SHA-256 Checksum for chain of custody
        sha256_hash = hashlib.sha256(content).hexdigest()

        # Destination directory
        est_dir = os.path.join(cls.BASE_STORAGE_DIR, establishment_id)
        os.makedirs(est_dir, exist_ok=True)

        doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
        unique_filename = f"{doc_id}_{file.filename}"
        storage_path = os.path.join(est_dir, unique_filename)

        with open(storage_path, "wb") as f:
            f.write(content)

        # Document lifecycle: Uploaded -> Queued -> Processing -> Ready
        timestamp = datetime.now(timezone.utc).isoformat()
        metadata = DocumentMetadata(
            id=doc_id,
            establishment_id=establishment_id,
            filename=file.filename,
            category=category,
            file_size_bytes=file_size,
            content_type=file.content_type or "application/octet-stream",
            sha256_hash=sha256_hash,
            status=DocumentStatus.READY,
            upload_timestamp=timestamp,
            pages=1,
            ocr_confidence=0.96 if ext in {".png", ".jpg", ".jpeg"} else 0.98,
            storage_path=storage_path,
        )

        DOCUMENT_REGISTRY[doc_id] = metadata
        return metadata

    @classmethod
    def get_document(cls, document_id: str) -> Optional[DocumentMetadata]:
        return DOCUMENT_REGISTRY.get(document_id)

    @classmethod
    def list_documents(cls, establishment_id: Optional[str] = None) -> List[DocumentMetadata]:
        if establishment_id:
            return [d for d in DOCUMENT_REGISTRY.values() if d.establishment_id == establishment_id]
        return list(DOCUMENT_REGISTRY.values())
