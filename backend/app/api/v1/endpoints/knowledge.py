from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.knowledge import LabourCodeSummary, StatutorySection, KnowledgeQueryResult
from app.rag.ingestion import KnowledgeBaseService

router = APIRouter()


@router.get("/codes", response_model=List[LabourCodeSummary], tags=["Labour Law Knowledge Base"])
async def list_labour_codes():
    """Returns catalog and summary metadata for the Four Enacted Indian Labour Codes."""
    return KnowledgeBaseService.list_codes()


@router.get("/codes/{code_id}", tags=["Labour Law Knowledge Base"])
async def get_labour_code_details(code_id: str):
    """Returns complete statutory provisions, chapters, and sections of a specific Labour Code."""
    code_data = KnowledgeBaseService.get_code_details(code_id)
    if not code_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Labour code '{code_id}' not found. Available codes: wages_2019, ir_2020, ss_2020, oshwc_2020",
        )
    return code_data


@router.get("/search", response_model=KnowledgeQueryResult, tags=["Labour Law Knowledge Base"])
async def search_labour_law_knowledge(
    q: str = Query(..., min_length=2, description="Search term, section number, or keyword"),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Searches the statutory Four Labour Codes knowledge base by section, legal concept, threshold, or penalty.
    """
    return KnowledgeBaseService.search_sections(query=q, limit=limit)
