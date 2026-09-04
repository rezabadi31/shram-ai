import os
from typing import Dict, Any, List, Optional
from app.schemas.extraction import DocumentIntelligenceResult
from app.document_ai.pdf_parser import PDFParserService
from app.document_ai.ocr_service import OCRFallbackService
from app.document_ai.table_extractor import TableExtractorService
from app.document_ai.upload import UploadService

# Cache for extracted results
EXTRACTION_CACHE: Dict[str, DocumentIntelligenceResult] = {}


class DocumentIntelligencePipeline:
    @classmethod
    def process_document(cls, document_id: str) -> DocumentIntelligenceResult:
        """
        Executes the dual-path extraction pipeline:
        Document -> Direct Text Extraction -> Quality Check -> Fallback OCR -> Table Extraction -> Structured JSON
        """
        doc = UploadService.get_document(document_id)
        if not doc:
            raise FileNotFoundError(f"Document ID '{document_id}' not found in registry")

        file_path = doc.storage_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Storage path '{file_path}' does not exist on disk")

        ext = os.path.splitext(file_path)[1].lower()

        # Tier 1: Attempt direct digital text extraction for PDFs
        if ext == ".pdf":
            pdf_result = PDFParserService.extract_text(file_path)
            if pdf_result.get("is_digital", False):
                full_text = "\n".join(pdf_result.get("pages", []))
                tables = TableExtractorService.parse_table_from_text(
                    text=full_text,
                    document_id=document_id,
                    page_number=1,
                    base_confidence=pdf_result.get("confidence", 0.98),
                )
                result = DocumentIntelligenceResult(
                    document_id=document_id,
                    document_type=doc.category.value,
                    filename=doc.filename,
                    pages=pdf_result.get("num_pages", 1),
                    overall_confidence=pdf_result.get("confidence", 0.98),
                    extraction_method="DIRECT_TEXT_EXTRACTION",
                    tables=tables,
                    extracted_records_count=sum([t.row_count for t in tables]),
                    raw_text_sample=full_text[:400] if full_text else "Direct digital stream extracted",
                )
                EXTRACTION_CACHE[document_id] = result
                return result

        # Tier 2: OCR Fallback for scanned PDFs or images
        ocr_result = OCRFallbackService.process_file(file_path)
        full_text = ocr_result.get("full_text", "")
        tables = TableExtractorService.parse_table_from_text(
            text=full_text,
            document_id=document_id,
            page_number=1,
            base_confidence=ocr_result.get("confidence", 0.93),
        )

        result = DocumentIntelligenceResult(
            document_id=document_id,
            document_type=doc.category.value,
            filename=doc.filename,
            pages=doc.pages,
            overall_confidence=ocr_result.get("confidence", 0.93),
            extraction_method="OCR_FALLBACK",
            tables=tables,
            extracted_records_count=sum([t.row_count for t in tables]),
            raw_text_sample=full_text[:400] if full_text else "OCR recognized text stream",
        )
        EXTRACTION_CACHE[document_id] = result
        return result

    @classmethod
    def get_cached_result(cls, document_id: str) -> Optional[DocumentIntelligenceResult]:
        return EXTRACTION_CACHE.get(document_id)
