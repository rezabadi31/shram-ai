from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GraphNodeType(str, Enum):
    ESTABLISHMENT = "ESTABLISHMENT"
    DOCUMENT = "DOCUMENT"
    RECORD = "RECORD"
    VIOLATION = "VIOLATION"
    CITATION = "CITATION"


class GraphEdgeType(str, Enum):
    CONTAINS = "CONTAINS"
    EXTRACTED_FROM = "EXTRACTED_FROM"
    VIOLATES = "VIOLATES"
    STATUTORY_SOURCE = "STATUTORY_SOURCE"


class EvidenceGraphNode(BaseModel):
    id: str
    label: str
    node_type: GraphNodeType
    tier: int  # 1 (Establishment) to 5 (Citation)
    properties: Dict[str, Any] = Field(default_factory=dict)


class EvidenceGraphEdge(BaseModel):
    source: str
    target: str
    edge_type: GraphEdgeType
    label: str


class EvidenceGraphResponse(BaseModel):
    establishment_id: str
    node_count: int
    edge_count: int
    nodes: List[EvidenceGraphNode]
    edges: List[EvidenceGraphEdge]


class ProvenancePathResponse(BaseModel):
    target_node_id: str
    path_node_ids: List[str]
    nodes: List[EvidenceGraphNode]
    edges: List[EvidenceGraphEdge]
    provenance_summary: str
