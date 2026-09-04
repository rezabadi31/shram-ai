from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RAGRetrievalMode(str, Enum):
    KEYWORD = "KEYWORD"
    SEMANTIC = "SEMANTIC"
    HYBRID = "HYBRID"


class StatutoryCitation(BaseModel):
    code_id: str
    act_title: str
    chapter: str
    section_number: str
    title: str
    citation_text: str
    authority: str
    penalty_summary: Optional[str] = None
    relevance_score: float


class RAGChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: Dict[str, Any]


class RAGQueryRequest(BaseModel):
    query: str
    mode: RAGRetrievalMode = RAGRetrievalMode.HYBRID
    limit: int = 4
    code_filter: Optional[str] = None


class RAGQueryResponse(BaseModel):
    query: str
    retrieval_mode: RAGRetrievalMode
    answer: str
    citations: List[StatutoryCitation]
    retrieved_chunks_count: int
    zero_hallucination_verified: bool = True
