import os
from typing import Dict, Any, List
from pypdf import PdfReader


class PDFParserService:
    @classmethod
    def extract_text(cls, file_path: str) -> Dict[str, Any]:
        """
        Direct digital text layer extraction from PDF files.
        Returns extracted text, page count, and character density to determine if OCR fallback is required.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            reader = PdfReader(file_path)
            pages_text: List[str] = []
            total_chars = 0

            for page in reader.pages:
                text = page.extract_text() or ""
                pages_text.append(text)
                total_chars += len(text.strip())

            num_pages = len(reader.pages)
            avg_chars_per_page = (total_chars / num_pages) if num_pages > 0 else 0

            # If average characters per page is greater than 50, it is a native digital PDF
            is_digital = avg_chars_per_page >= 50

            return {
                "pages": pages_text,
                "num_pages": num_pages,
                "total_chars": total_chars,
                "is_digital": is_digital,
                "confidence": 0.98 if is_digital else 0.40,
            }
        except Exception as e:
            return {
                "pages": [],
                "num_pages": 1,
                "total_chars": 0,
                "is_digital": False,
                "confidence": 0.0,
                "error": str(e),
            }
