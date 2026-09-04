from app.evidence_graph.graph_builder import EvidenceGraphBuilder
from app.schemas.evidence_graph import GraphNodeType


def test_build_establishment_graph_tiers():
    graph = EvidenceGraphBuilder.build_establishment_graph(establishment_id="EST-001")
    assert graph.establishment_id == "EST-001"
    assert graph.node_count >= 10
    assert graph.edge_count >= 10

    # Verify all 5 tiers exist
    tiers = {n.tier for n in graph.nodes}
    assert {1, 2, 3, 4, 5}.issubset(tiers)

    # Verify node types
    node_types = {n.node_type for n in graph.nodes}
    assert GraphNodeType.ESTABLISHMENT in node_types
    assert GraphNodeType.DOCUMENT in node_types
    assert GraphNodeType.RECORD in node_types
    assert GraphNodeType.VIOLATION in node_types
    assert GraphNodeType.CITATION in node_types


def test_evidence_graph_provenance_path():
    # Provenance path for Minimum Wage violation
    prov = EvidenceGraphBuilder.get_provenance_path(
        establishment_id="EST-001",
        target_node_id="VIO-MIN_WAGE",
    )
    assert prov.target_node_id == "VIO-MIN_WAGE"
    assert len(prov.path_node_ids) >= 3
    assert prov.path_node_ids[0] == "EST-001"
    assert "VIO-MIN_WAGE" in prov.path_node_ids
    assert len(prov.provenance_summary) > 5

    # Provenance path for Ghost Worker anomaly
    prov_ghost = EvidenceGraphBuilder.get_provenance_path(
        establishment_id="EST-001",
        target_node_id="ANOM-GHOST",
    )
    assert "ANOM-GHOST" in prov_ghost.path_node_ids


def test_evidence_graph_api_endpoints(client):
    # GET full graph
    resp = client.get("/api/v1/evidence-graph/EST-001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["establishment_id"] == "EST-001"
    assert len(data["nodes"]) >= 10
    assert len(data["edges"]) >= 10

    # GET provenance path
    prov_resp = client.get("/api/v1/evidence-graph/EST-001/provenance/VIO-MIN_WAGE")
    assert prov_resp.status_code == 200
    prov_data = prov_resp.json()
    assert prov_data["target_node_id"] == "VIO-MIN_WAGE"
    assert len(prov_data["nodes"]) >= 3
    assert "Lineage" in prov_data["provenance_summary"] or "lineage" in prov_data["provenance_summary"]
