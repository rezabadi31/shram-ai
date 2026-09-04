from fastapi import APIRouter, Path, Query
from app.schemas.evidence_graph import EvidenceGraphResponse, ProvenancePathResponse
from app.evidence_graph.graph_builder import EvidenceGraphBuilder

router = APIRouter()


@router.get("/{establishment_id}", response_model=EvidenceGraphResponse, tags=["Evidence Graph Model"])
async def get_evidence_graph(
    establishment_id: str = Path(..., description="Target establishment ID"),
    establishment_name: str = Query("ABC Industries Ltd.", description="Establishment name"),
):
    """
    Retrieves the 5-tier directed Evidence Graph for an establishment:
    Tier 1 (Establishment) ➔ Tier 2 (Documents) ➔ Tier 3 (Records) ➔ Tier 4 (Violations) ➔ Tier 5 (Citations).
    """
    return EvidenceGraphBuilder.build_establishment_graph(
        establishment_id=establishment_id,
        establishment_name=establishment_name,
    )


@router.get("/{establishment_id}/provenance/{node_id}", response_model=ProvenancePathResponse, tags=["Evidence Graph Model"])
async def get_provenance_path(
    establishment_id: str = Path(..., description="Target establishment ID"),
    node_id: str = Path(..., description="Target node ID to trace provenance for"),
):
    """
    Traces the provenance lineage from the establishment root down to the target violation or citation node.
    Enables explainability: every risk finding traces back to raw document bounding boxes and rows.
    """
    return EvidenceGraphBuilder.get_provenance_path(
        establishment_id=establishment_id,
        target_node_id=node_id,
    )
