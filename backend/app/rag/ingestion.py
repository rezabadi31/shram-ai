import os
import json
from typing import List, Dict, Any, Optional
from app.schemas.knowledge import (
    LabourCodeSummary,
    StatutorySection,
    StatutoryThreshold,
    PenaltyStructure,
    KnowledgeQueryResult,
)

KNOWLEDGE_BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "knowledge_base")
)


class KnowledgeBaseService:
    _loaded = False
    _codes_summary: Dict[str, LabourCodeSummary] = {}
    _all_sections: List[StatutorySection] = []
    _full_datasets: Dict[str, dict] = {}

    @classmethod
    def load_knowledge_base(cls):
        """Loads and indexes the Four Labour Codes structured datasets from disk."""
        if cls._loaded:
            return

        cls._codes_summary.clear()
        cls._all_sections.clear()
        cls._full_datasets.clear()

        filenames = [
            "code_on_wages_2019.json",
            "industrial_relations_code_2020.json",
            "social_security_code_2020.json",
            "oshwc_code_2020.json",
        ]

        for fname in filenames:
            fpath = os.path.join(KNOWLEDGE_BASE_DIR, fname)
            if not os.path.exists(fpath):
                continue

            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            summary_data = data.get("summary", {})
            code_id = summary_data.get("code_id")
            if not code_id:
                continue

            summary = LabourCodeSummary(**summary_data)
            cls._codes_summary[code_id] = summary
            cls._full_datasets[code_id] = data

            for s_data in data.get("sections", []):
                sec = StatutorySection(**s_data)
                cls._all_sections.append(sec)

        cls._loaded = True

    @classmethod
    def list_codes(cls) -> List[LabourCodeSummary]:
        cls.load_knowledge_base()
        return list(cls._codes_summary.values())

    @classmethod
    def get_code_details(cls, code_id: str) -> Optional[dict]:
        cls.load_knowledge_base()
        return cls._full_datasets.get(code_id)

    @classmethod
    def get_section(cls, code_id: str, section_number: str) -> Optional[StatutorySection]:
        cls.load_knowledge_base()
        clean_target = section_number.lower().replace("section", "").replace("sec", "").replace(".", "").strip()
        for s in cls._all_sections:
            if s.code_id == code_id:
                clean_sec = s.section_number.lower().replace("section", "").replace("sec", "").replace(".", "").strip()
                if clean_sec == clean_target:
                    return s
        return None

    @classmethod
    def search_sections(cls, query: str, limit: int = 10) -> KnowledgeQueryResult:
        cls.load_knowledge_base()
        q_tokens = [t.lower().strip() for t in query.split() if len(t.strip()) > 2]
        if not q_tokens:
            return KnowledgeQueryResult(query=query, total_matches=len(cls._all_sections), results=cls._all_sections[:limit])

        scored_matches = []
        for sec in cls._all_sections:
            score = 0
            text_corpus = f"{sec.code_name} {sec.chapter_title} {sec.section_number} {sec.title} {sec.statutory_text} {' '.join(sec.keywords)}".lower()

            # Exact section match boost
            if query.lower() in sec.section_number.lower() or query.lower() in sec.title.lower():
                score += 50

            for token in q_tokens:
                if token in sec.section_number.lower():
                    score += 20
                if token in sec.title.lower():
                    score += 15
                if any(token in kw.lower() for kw in sec.keywords):
                    score += 10
                if token in text_corpus:
                    score += 2

            if score > 0:
                scored_matches.append((score, sec))

        # Sort by relevance score descending
        scored_matches.sort(key=lambda x: x[0], reverse=True)
        results = [m[1] for m in scored_matches[:limit]]
        return KnowledgeQueryResult(
            query=query,
            total_matches=len(scored_matches),
            results=results,
        )
