from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ExtractionProvenance(BaseModel):
    document_id: str
    page: int
    table_index: int = 0
    confidence: float
    bounding_box: Optional[List[float]] = None  # [x1, y1, x2, y2]


class ExtractedTableRow(BaseModel):
    row_index: int
    values: Dict[str, Any]
    provenance: ExtractionProvenance


class ExtractedTable(BaseModel):
    table_name: str
    headers: List[str]
    rows: List[ExtractedTableRow]
    row_count: int


class DocumentIntelligenceResult(BaseModel):
    document_id: str
    document_type: str
    filename: str
    pages: int
    overall_confidence: float
    extraction_method: str  # DIRECT_TEXT_EXTRACTION or OCR_FALLBACK
    tables: List[ExtractedTable]
    extracted_records_count: int
    raw_text_sample: str
