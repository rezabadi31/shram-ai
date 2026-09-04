from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ModelEvaluationMetrics(BaseModel):
    model_name: str
    algorithm: str
    roc_auc: float
    precision: float
    recall: float
    f1_score: float
    rmse: float
    r2_score: float
    training_time_ms: float
    is_champion: bool = False


class ModelBenchmarkComparison(BaseModel):
    models: List[ModelEvaluationMetrics]
    champion_model: str
    total_training_samples: int
    total_testing_samples: int
    benchmark_timestamp: str


class ModelTrainingResponse(BaseModel):
    status: str
    message: str
    benchmark: ModelBenchmarkComparison


class RiskPredictionRequest(BaseModel):
    establishment_id: Optional[str] = "EST-001"
    worker_count: Optional[int] = None
    contract_worker_ratio: Optional[float] = None
    hazardous_process: Optional[bool] = None
    industry_sector: Optional[str] = None
    wage_violation_count: Optional[int] = None
    ot_violation_count: Optional[int] = None
    deduction_violation_count: Optional[int] = None
    missing_register_count: Optional[int] = None
    ghost_worker_count: Optional[int] = None
    uncompensated_worker_count: Optional[int] = None
    disbursement_mismatch_count: Optional[int] = None


class RiskPredictionResponse(BaseModel):
    establishment_id: str
    ml_model: str
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_probability: float = Field(..., ge=0.0, le=1.0)
    priority_class: str  # HIGH, MEDIUM, LOW
    percentile: str
    confidence_score: float
    calibrated_action: str
