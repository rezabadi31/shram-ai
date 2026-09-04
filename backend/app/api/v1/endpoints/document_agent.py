from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, Body
from app.schemas.document_agent import DocumentAgentAuditResult
from app.agents.document_agent import DocumentAgentService

router = APIRouter()


@router.post("/audit", response_model=DocumentAgentAuditResult, tags=["Document Agent"])
async def run_document_agent_audit(
    establishment_id: str = Query("EST-001", description="Target establishment ID"),
    payload: Optional[Dict[str, Any]] = Body(default=None),
):
    """
    Executes autonomous Document Agent audit:
    - Calculates scan legibility confidence
    - Checks structural completeness
    - Compares uploaded registers against legally mandated statutory filings
    - Pinpoints missing registers and penalty exposures
    """
    uploaded_documents = payload.get("uploaded_documents") if payload else None
    worker_count = payload.get("worker_count", 420) if payload else 420
    industry = payload.get("industry", "Automobile Component Manufacturing") if payload else "Automobile Component Manufacturing"

    return DocumentAgentService.run_document_audit(
        establishment_id=establishment_id,
        uploaded_documents=uploaded_documents,
        worker_count=worker_count,
        industry=industry,
    )


@router.get("/required-registers", tags=["Document Agent"])
async def get_required_registers(
    worker_count: int = Query(420, ge=1),
    industry: str = Query("Automobile Component Manufacturing"),
    has_hazardous_process: bool = Query(False),
):
    """
    Returns dynamically calculated statutory register filing schedule under the Four Labour Codes
    based on headcount, industry sector, and hazardous processes.
    """
    return DocumentAgentService.determine_required_registers(
        worker_count=worker_count,
        industry=industry,
        has_hazardous_process=has_hazardous_process,
    )
