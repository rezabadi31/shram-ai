import networkx as nx
from typing import Dict, Any, List, Optional
from app.schemas.evidence_graph import (
    GraphNodeType,
    GraphEdgeType,
    EvidenceGraphNode,
    EvidenceGraphEdge,
    EvidenceGraphResponse,
    ProvenancePathResponse,
)


class EvidenceGraphBuilder:
    @classmethod
    def build_establishment_graph(
        cls,
        establishment_id: str = "EST-001",
        establishment_name: str = "ABC Industries Ltd.",
    ) -> EvidenceGraphResponse:
        """
        Builds a 5-tier directed Evidence Graph:
        Tier 1: Establishment
        Tier 2: Documents (Form B, Form D, Bank Scroll)
        Tier 3: Extracted Canonical Records (Rows)
        Tier 4: Rule Violations & Cross-Doc Anomalies
        Tier 5: Statutory Citations (Code on Wages, OSHWC)
        """
        G = nx.DiGraph()

        # Tier 1: Establishment Root
        G.add_node(
            establishment_id,
            label=f"Establishment: {establishment_name}",
            node_type=GraphNodeType.ESTABLISHMENT,
            tier=1,
            properties={"sector": "Automobile Manufacturing", "workforce": 420, "risk_category": "HIGH"},
        )

        # Tier 2: Audited Documents
        docs = [
            ("DOC-001", "Form B - Register of Wages (Oct 2024)", "PDF Wage Register", 14),
            ("DOC-002", "Form D - Muster Roll (Oct 2024)", "Attendance Muster", 8),
            ("DOC-003", "Disbursement Scroll - Axis Bank UTR", "Bank Statement", 4),
        ]
        for doc_id, doc_label, doc_cat, pages in docs:
            G.add_node(
                doc_id,
                label=doc_label,
                node_type=GraphNodeType.DOCUMENT,
                tier=2,
                properties={"category": doc_cat, "pages": pages},
            )
            G.add_edge(establishment_id, doc_id, edge_type=GraphEdgeType.CONTAINS, label="filed_by")

        # Tier 3: Canonical Worker Records
        records = [
            ("REC-EMP003", "Record: EMP-003 (Rajesh K.)", "DOC-001", {"daily_rate": 310.0, "gross_wages": 8060.0, "ot_hours": 12.0, "deductions": 800.0}),
            ("REC-EMP009", "Record: EMP-009 (Vikram Singh)", "DOC-001", {"gross_wages": 16500.0, "deductions": 1000.0}),
            ("REC-ATT009", "Attendance: EMP-009", "DOC-002", {"days_present": 0, "status": "ABSENT_ALL_DAYS"}),
            ("REC-BNK003", "Bank Payout: EMP-003", "DOC-003", {"amount": 6260.0, "utr": "AXIS241029001"}),
        ]
        for rec_id, rec_label, parent_doc, props in records:
            G.add_node(
                rec_id,
                label=rec_label,
                node_type=GraphNodeType.RECORD,
                tier=3,
                properties=props,
            )
            G.add_edge(parent_doc, rec_id, edge_type=GraphEdgeType.EXTRACTED_FROM, label="extracted_from")

        # Tier 4: Violations & Anomalies
        violations = [
            (
                "VIO-MIN_WAGE",
                "Violation: Below Minimum Floor Wage (₹310 vs ₹450)",
                ["REC-EMP003"],
                {"severity": "HIGH", "deficit": "₹140/day"},
            ),
            (
                "VIO-OVERTIME",
                "Violation: Overtime Below Double Rate (₹450 vs ₹930)",
                ["REC-EMP003"],
                {"severity": "HIGH", "deficit": "₹480 deficit"},
            ),
            (
                "ANOM-GHOST",
                "Anomaly: Ghost Worker (Wage Paid, 0 Attendance)",
                ["REC-EMP009", "REC-ATT009"],
                {"severity": "HIGH", "amount": "₹16,500.00"},
            ),
            (
                "ANOM-SKIM",
                "Anomaly: Net Disbursement Mismatch (₹1,000 Skimmed)",
                ["REC-EMP003", "REC-BNK003"],
                {"severity": "HIGH", "diverted": "₹1,000.00"},
            ),
        ]
        for vio_id, vio_label, connected_recs, props in violations:
            G.add_node(
                vio_id,
                label=vio_label,
                node_type=GraphNodeType.VIOLATION,
                tier=4,
                properties=props,
            )
            for rec_id in connected_recs:
                G.add_edge(rec_id, vio_id, edge_type=GraphEdgeType.VIOLATES, label="exhibits_violation")

        # Tier 5: Statutory Citations (Labour Law RAG ground truth)
        citations = [
            ("CIT-WAGES-SEC6", "Code on Wages, 2019 • Sec. 6 & 8", "VIO-MIN_WAGE", {"act": "Code on Wages 2019", "penalty": "Fine up to ₹50,000"}),
            ("CIT-WAGES-SEC14", "Code on Wages, 2019 • Sec. 14 (Overtime 2x)", "VIO-OVERTIME", {"act": "Code on Wages 2019", "penalty": "Fine up to ₹20,000"}),
            ("CIT-WAGES-SEC50", "Code on Wages, 2019 • Sec. 50 (Registers & Fraud)", "ANOM-GHOST", {"act": "Code on Wages 2019", "penalty": "Fine up to ₹20,000 / Fraud prosecution"}),
            ("CIT-WAGES-SEC18", "Code on Wages, 2019 • Sec. 18 (Deductions Ceiling)", "ANOM-SKIM", {"act": "Code on Wages 2019", "penalty": "Fine up to ₹20,000"}),
        ]
        for cit_id, cit_label, parent_vio, props in citations:
            G.add_node(
                cit_id,
                label=cit_label,
                node_type=GraphNodeType.CITATION,
                tier=5,
                properties=props,
            )
            G.add_edge(parent_vio, cit_id, edge_type=GraphEdgeType.STATUTORY_SOURCE, label="governed_by")

        # Convert to Response schemas
        nodes_list: List[EvidenceGraphNode] = []
        for n, data in G.nodes(data=True):
            nodes_list.append(
                EvidenceGraphNode(
                    id=n,
                    label=data.get("label", n),
                    node_type=data.get("node_type", GraphNodeType.RECORD),
                    tier=data.get("tier", 3),
                    properties=data.get("properties", {}),
                )
            )

        edges_list: List[EvidenceGraphEdge] = []
        for u, v, data in G.edges(data=True):
            edges_list.append(
                EvidenceGraphEdge(
                    source=u,
                    target=v,
                    edge_type=data.get("edge_type", GraphEdgeType.CONTAINS),
                    label=data.get("label", ""),
                )
            )

        return EvidenceGraphResponse(
            establishment_id=establishment_id,
            node_count=len(nodes_list),
            edge_count=len(edges_list),
            nodes=nodes_list,
            edges=edges_list,
        )

    @classmethod
    def get_provenance_path(
        cls,
        establishment_id: str = "EST-001",
        target_node_id: str = "VIO-MIN_WAGE",
    ) -> ProvenancePathResponse:
        """
        Traces the exact provenance path from Establishment root down to the target node
        (e.g., Establishment -> Form B -> Row 3 -> Minimum Wage Violation -> Statutory Citation).
        """
        graph_resp = cls.build_establishment_graph(establishment_id=establishment_id)
        
        # Reconstruct nx graph
        G = nx.DiGraph()
        node_lookup = {n.id: n for n in graph_resp.nodes}
        for n in graph_resp.nodes:
            G.add_node(n.id, **n.model_dump())
        for e in graph_resp.edges:
            G.add_edge(e.source, e.target, **e.model_dump())

        path_nodes: List[str] = []
        try:
            # Shortest path from root establishment to target node
            if nx.has_path(G, establishment_id, target_node_id):
                path_nodes = nx.shortest_path(G, establishment_id, target_node_id)
            elif nx.has_path(G, target_node_id, establishment_id):
                path_nodes = list(reversed(nx.shortest_path(G, target_node_id, establishment_id)))
            else:
                path_nodes = [establishment_id, target_node_id]
        except Exception:
            path_nodes = [establishment_id, target_node_id]

        path_node_objs = [node_lookup[nid] for nid in path_nodes if nid in node_lookup]
        path_edge_objs = [
            e for e in graph_resp.edges
            if e.source in path_nodes and e.target in path_nodes
        ]

        summary = f"Trace lineage: {' ➔ '.join([n.label.split(':')[0] for n in path_node_objs])}"

        return ProvenancePathResponse(
            target_node_id=target_node_id,
            path_node_ids=path_nodes,
            nodes=path_node_objs,
            edges=path_edge_objs,
            provenance_summary=summary,
        )
