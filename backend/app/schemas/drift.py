from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class FeatureDriftMetric(BaseModel):
    feature_name: str
    baseline_mean: float
    current_mean: float
    psi_score: float  # Population Stability Index: <0.1 No drift, 0.1-0.25 Moderate, >0.25 Significant
    drift_status: str  # NO_DRIFT | MODERATE_DRIFT | SIGNIFICANT_DRIFT
    p_value: float


class ModelDriftReport(BaseModel):
    report_id: str
    timestamp: str
    model_version: str
    overall_psi: float
    drift_alert_level: str  # GREEN | YELLOW | RED
    inspections_ingested_count: int
    inspector_override_rate: float  # % of inspection items modified by human officers
    total_feedback_records: int
    feature_drifts: List[FeatureDriftMetric]
    calibration_brier_score: float
    recommended_action: str
    metadata: Optional[Dict[str, Any]] = None


class RetrainTriggerRequest(BaseModel):
    trigger_reason: Optional[str] = "SCHEDULED_DRIFT_CALIBRATION"
    include_inspector_feedback: Optional[bool] = True
    challenger_algorithm: Optional[str] = "xgboost"


class RetrainTriggerResponse(BaseModel):
    job_id: str
    status: str
    trained_at: str
    samples_used: int
    feedback_samples_incorporated: int
    champion_auc: float
    challenger_auc: float
    deployed_model: str
    improvement_delta: float
    message: str
