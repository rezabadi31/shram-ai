from typing import List
from app.schemas.rag import RAGChunk
from app.schemas.knowledge import StatutorySection
from app.rag.ingestion import KnowledgeBaseService


class StatutoryChunker:
    @classmethod
    def get_chunks_for_all_codes(cls) -> List[RAGChunk]:
        """
        Creates semantic statutory chunks from the Four Labour Codes.
        Each chunk encapsulates the act, section number, title, text, and penalties.
        """
        KnowledgeBaseService.load_knowledge_base()
        sections = KnowledgeBaseService._all_sections
        chunks: List[RAGChunk] = []

        for idx, sec in enumerate(sections):
            chunk_text = (
                f"Statute: {sec.code_name} ({sec.code_id})\n"
                f"Chapter: {sec.chapter_number} - {sec.chapter_title}\n"
                f"Section: {sec.section_number} - {sec.title}\n"
                f"Statutory Text: {sec.statutory_text}\n"
                f"Keywords: {', '.join(sec.keywords)}\n"
            )
            if sec.thresholds:
                chunk_text += f"Applicability: {sec.thresholds.applicability_limit} ({sec.thresholds.enforcing_authority})\n"
            if sec.penalties:
                chunk_text += f"Penalties: 1st Offense: {sec.penalties.first_offense_fine}; Subsequent: {sec.penalties.subsequent_offense}\n"

            chunk = RAGChunk(
                chunk_id=f"CHK-{sec.code_id}-{sec.section_number.replace(' ', '_')}-{idx}",
                text=chunk_text,
                metadata={
                    "code_id": sec.code_id,
                    "code_name": sec.code_name,
                    "chapter": sec.chapter_title,
                    "section_number": sec.section_number,
                    "title": sec.title,
                    "authority": sec.thresholds.enforcing_authority if sec.thresholds else "Inspector-cum-Facilitator",
                    "penalties": f"1st: {sec.penalties.first_offense_fine}" if sec.penalties else None,
                    "citation": sec.citation,
                    "statutory_text": sec.statutory_text,
                },
            )
            chunks.append(chunk)

        return chunks
