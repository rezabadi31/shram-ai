from typing import Optional
from fastapi import APIRouter, Body
from app.schemas.models import (
    ModelBenchmarkComparison,
    ModelTrainingResponse,
    RiskPredictionRequest,
    RiskPredictionResponse,
)
from app.ml.model_trainer import MLRiskModelTrainer

router = APIRouter()


@router.post("/train", response_model=ModelTrainingResponse, tags=["ML Risk Models"])
async def train_ml_models():
    """
    Trains and benchmarks XGBoost, Random Forest, and Logistic Regression on the
    22-dimensional feature matrix, saving champion model artifacts in models/.
    """
    return MLRiskModelTrainer.train_and_benchmark()


@router.get("/benchmark", response_model=ModelBenchmarkComparison, tags=["ML Risk Models"])
async def get_model_benchmark():
    """
    Returns comparative evaluation metrics (ROC-AUC, Precision, Recall, F1, RMSE, Latency)
    across XGBoost, Random Forest, and Logistic Regression.
    """
    return MLRiskModelTrainer.get_benchmark_report()


@router.post("/predict", response_model=RiskPredictionResponse, tags=["ML Risk Models"])
async def predict_establishment_risk(request: Optional[RiskPredictionRequest] = Body(default=None)):
    """
    Runs deterministic real-time ML risk scoring inference using the trained champion XGBoost model.
    Mandate: ML MODEL determines score. LLM explains score.
    """
    req = request or RiskPredictionRequest()
    return MLRiskModelTrainer.predict_risk(
        establishment_id=req.establishment_id or "EST-001",
        worker_count=req.worker_count,
        contract_worker_ratio=req.contract_worker_ratio,
        hazardous_process=req.hazardous_process,
        industry_sector=req.industry_sector,
        wage_violation_count=req.wage_violation_count,
        ot_violation_count=req.ot_violation_count,
        deduction_violation_count=req.deduction_violation_count,
        missing_register_count=req.missing_register_count,
        ghost_worker_count=req.ghost_worker_count,
        uncompensated_worker_count=req.uncompensated_worker_count,
        disbursement_mismatch_count=req.disbursement_mismatch_count,
    )
