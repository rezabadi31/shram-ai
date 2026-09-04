from typing import Optional
from fastapi import APIRouter, Body
from app.schemas.risk_agent import (
    RiskAgentAuditRequest,
    RiskAgentAuditResult,
    RiskThresholdsResponse,
)
from app.agents.risk_agent import RiskAgentService

router = APIRouter()


@router.post("/evaluate", response_model=RiskAgentAuditResult, tags=["Risk Agent"])
async def run_risk_agent_audit(request: Optional[RiskAgentAuditRequest] = Body(default=None)):
    """
    Runs the Risk Agent audit pipeline on an establishment.
    Combines calibrated XGBoost prediction, TreeSHAP feature attributions, and evidence graph nodes
    to synthesize actionable enforcement directives and priority framing.
    Strict Directive: 'ML MODEL determines score. LLM explains score.'
    """
    req = request or RiskAgentAuditRequest()
    return RiskAgentService.evaluate_establishment_risk(
        establishment_id=req.establishment_id,
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


@router.get("/thresholds", response_model=RiskThresholdsResponse, tags=["Risk Agent"])
async def get_calibrated_risk_thresholds():
    """
    Returns calibrated jurisdiction risk classification thresholds for inspection queue prioritization.
    """
    return RiskAgentService.get_risk_thresholds()
