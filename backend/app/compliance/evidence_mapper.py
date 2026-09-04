"""Evidence mapper: Links extracted document fields to legal rule criteria."""
from typing import Dict, Any


class EvidenceMapper:
    def map_evidence(self, document_id: str, page_num: int, field_name: str, value: Any) -> Dict[str, Any]:
        return {
            "source_document": document_id,
            "page": page_num,
            "field": field_name,
            "value": value,
        }
