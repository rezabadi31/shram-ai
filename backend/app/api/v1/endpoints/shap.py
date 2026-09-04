from typing import Optional
from fastapi import APIRouter, Body, Query
from app.schemas.shap import (
    ShapLocalExplanationResponse,
    ShapGlobalSummaryResponse,
)
from app.schemas.models import RiskPredictionRequest
from app.ml.shap_explainer import ShapExplainerService

router = APIRouter()


@router.post("/explain", response_model=ShapLocalExplanationResponse, tags=["Explainable AI (SHAP)"])
async def explain_establishment_risk(request: Optional[RiskPredictionRequest] = Body(default=None)):
    """
    Computes local TreeSHAP feature attributions for an establishment.
    Explains which factors push the predicted risk score UP (escalators) vs DOWN (mitigators).
    Enforces additivity: Predicted Score = Base Value + sum(Shapley values).
    """
    req = request or RiskPredictionRequest()
    return ShapExplainerService.explain_establishment(
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


@router.get("/global-importance", response_model=ShapGlobalSummaryResponse, tags=["Explainable AI (SHAP)"])
async def get_global_feature_importance(max_samples: int = Query(100, ge=10, le=500)):
    """
    Returns global feature importance ranked by mean absolute TreeSHAP value
    across the establishment compliance benchmark dataset.
    """
    return ShapExplainerService.compute_global_importance(max_samples=max_samples)
