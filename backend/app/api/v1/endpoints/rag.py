from fastapi import APIRouter
from app.schemas.rag import RAGQueryRequest, RAGQueryResponse
from app.rag.retrieval import HybridRetriever

router = APIRouter()


@router.post("/query", response_model=RAGQueryResponse, tags=["Labour Law RAG Engine"])
async def query_labour_rag(request: RAGQueryRequest):
    """
    Query the statutory Indian Labour Law RAG engine.
    Supports KEYWORD, SEMANTIC, and HYBRID (RRF Re-ranking) retrieval modes with zero hallucination.
    """
    return HybridRetriever.query(
        query=request.query,
        mode=request.mode,
        limit=request.limit,
    )
