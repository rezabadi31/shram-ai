from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class DocumentCategory(str, Enum):
    WAGE_REGISTER = "Wage Register"
    ATTENDANCE_REGISTER = "Attendance Register"
    EMPLOYEE_REGISTER = "Employee Register"
    PAYROLL = "Payroll"
    SAFETY_RECORD = "Safety Record"
    RETURN = "Return"
    EMPLOYMENT_CONTRACT = "Employment Contract"
    OTHER = "Other"


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    OCR_COMPLETED = "OCR_COMPLETED"
    STRUCTURED = "STRUCTURED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    READY = "READY"


class DocumentMetadata(BaseModel):
    id: str
    establishment_id: str
    filename: str
    category: DocumentCategory
    file_size_bytes: int
    content_type: str
    sha256_hash: str
    status: DocumentStatus
    upload_timestamp: str
    pages: int = 1
    ocr_confidence: float = 0.95
    storage_path: str


class DocumentUploadResponse(BaseModel):
    message: str
    document: DocumentMetadata


class DocumentListResponse(BaseModel):
    total: int
    documents: List[DocumentMetadata]
