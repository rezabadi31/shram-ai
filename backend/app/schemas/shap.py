from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ShapFeatureContribution(BaseModel):
    feature_name: str
    feature_label: str
    category: str
    feature_value: float
    shap_value: float
    direction: str  # "positive" (risk escalator) or "negative" (risk mitigator)
    explanation: str


class ShapLocalExplanationResponse(BaseModel):
    establishment_id: str
    base_value: float = Field(..., description="Actuarial jurisdiction expected baseline risk E[f(X)]")
    predicted_risk_score: float = Field(..., description="Final calibrated ML model risk score")
    net_shap_adjustment: float = Field(..., description="Sum of all feature Shapley contributions")
    positive_escalators: List[ShapFeatureContribution]
    negative_mitigators: List[ShapFeatureContribution]
    all_contributions: List[ShapFeatureContribution]


class ShapGlobalFeatureImportanceItem(BaseModel):
    feature_name: str
    feature_label: str
    category: str
    mean_abs_shap: float
    rank: int


class ShapGlobalSummaryResponse(BaseModel):
    dataset_size: int
    feature_count: int
    top_features: List[ShapGlobalFeatureImportanceItem]
