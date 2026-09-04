from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class FeatureCategory(str, Enum):
    DEMOGRAPHIC = "DEMOGRAPHIC"
    DETERMINISTIC = "DETERMINISTIC"
    ANOMALY = "ANOMALY"
    HISTORICAL = "HISTORICAL"
    INTERACTION = "INTERACTION"


class FeatureDefinition(BaseModel):
    name: str
    label: str
    category: FeatureCategory
    description: str
    formula: str
    weight_hint: float


class FeatureVectorItem(BaseModel):
    name: str
    label: str
    category: FeatureCategory
    raw_value: float
    normalized_value: float
    formula: str


class FeatureExtractionRequest(BaseModel):
    establishment_id: Optional[str] = "EST-001"
    worker_count: Optional[int] = None
    contract_worker_ratio: Optional[float] = None
    female_worker_ratio: Optional[float] = None
    hazardous_process: Optional[bool] = None
    industry_sector: Optional[str] = None
    wage_violation_count: Optional[int] = None
    ot_violation_count: Optional[int] = None
    deduction_violation_count: Optional[int] = None
    missing_register_count: Optional[int] = None
    ghost_worker_count: Optional[int] = None
    uncompensated_worker_count: Optional[int] = None
    disbursement_mismatch_count: Optional[int] = None
    inspection_history_violations: Optional[int] = None
    grievance_complaint_count: Optional[int] = None


class FeatureExtractionResponse(BaseModel):
    establishment_id: str
    feature_count: int = 22
    features: List[FeatureVectorItem]
    vector: Dict[str, float]


class FeatureSummaryStats(BaseModel):
    name: str
    label: str
    category: FeatureCategory
    mean: float
    std: float
    min_val: float
    max_val: float


class DatasetFeatureMatrixSummary(BaseModel):
    sample_count: int
    feature_count: int
    features: List[FeatureSummaryStats]
