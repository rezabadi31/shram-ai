from typing import List, Optional
from fastapi import APIRouter, Query, Body, HTTPException
from app.schemas.features import (
    FeatureDefinition,
    FeatureExtractionRequest,
    FeatureExtractionResponse,
    DatasetFeatureMatrixSummary,
)
from app.ml.feature_extractor import RiskFeatureExtractor

router = APIRouter()


@router.get("/definitions", response_model=List[FeatureDefinition], tags=["ML Feature Engineering"])
async def get_feature_definitions():
    """
    Returns the complete registry of 22 engineered risk features, formulas, categories, and descriptions.
    """
    return RiskFeatureExtractor.get_feature_definitions()


@router.post("/extract", response_model=FeatureExtractionResponse, tags=["ML Feature Engineering"])
async def extract_features(request: Optional[FeatureExtractionRequest] = Body(default=None)):
    """
    Extracts the 22-dimensional normalized feature vector for a specified establishment or customized input parameters.
    """
    req = request or FeatureExtractionRequest()
    return RiskFeatureExtractor.extract_features(
        establishment_id=req.establishment_id or "EST-001",
        worker_count=req.worker_count if req.worker_count is not None else 420,
        contract_worker_ratio=req.contract_worker_ratio if req.contract_worker_ratio is not None else 0.42,
        female_worker_ratio=req.female_worker_ratio if req.female_worker_ratio is not None else 0.28,
        hazardous_process=req.hazardous_process if req.hazardous_process is not None else True,
        industry_sector=req.industry_sector or "Automobile & Auto Components",
        wage_violation_count=req.wage_violation_count if req.wage_violation_count is not None else 3,
        ot_violation_count=req.ot_violation_count if req.ot_violation_count is not None else 2,
        deduction_violation_count=req.deduction_violation_count if req.deduction_violation_count is not None else 1,
        missing_register_count=req.missing_register_count if req.missing_register_count is not None else 2,
        ghost_worker_count=req.ghost_worker_count if req.ghost_worker_count is not None else 1,
        uncompensated_worker_count=req.uncompensated_worker_count if req.uncompensated_worker_count is not None else 1,
        disbursement_mismatch_count=req.disbursement_mismatch_count if req.disbursement_mismatch_count is not None else 1,
        inspection_history_violations=req.inspection_history_violations if req.inspection_history_violations is not None else 2,
        grievance_complaint_count=req.grievance_complaint_count if req.grievance_complaint_count is not None else 1,
    )


@router.get("/matrix-summary", response_model=DatasetFeatureMatrixSummary, tags=["ML Feature Engineering"])
async def get_feature_matrix_summary():
    """
    Returns dataset-wide statistical distribution (mean, standard deviation, min, max)
    across all 22 engineered features for the 1,000+ establishments dataset.
    """
    return RiskFeatureExtractor.compute_matrix_summary()
