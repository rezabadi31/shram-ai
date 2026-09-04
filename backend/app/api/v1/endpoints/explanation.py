from fastapi import APIRouter
from app.schemas.explanation import (
    ExplanationGenerationRequest,
    ComprehensiveExplanationResponse,
    InspectorExplanationBrief,
    EmployerRemediationPlan,
)
from app.explanation.generator import ExplanationService

router = APIRouter()


@router.post("/generate", response_model=ComprehensiveExplanationResponse)
def generate_comprehensive_explanation(request: ExplanationGenerationRequest):
    """
    Generates dual-audience natural language explanation package for an establishment.
    Combines calibrated ML risk score, TreeSHAP attributions, statutory violations,
    and cross-document anomalies into tailored Inspector and Employer narratives.
    """
    return ExplanationService.generate_comprehensive_explanation(
        establishment_id=request.establishment_id,
        worker_count=request.worker_count,
        wage_violation_count=request.wage_violation_count,
        ghost_worker_count=request.ghost_worker_count,
    )


@router.post("/inspector-brief", response_model=InspectorExplanationBrief)
def generate_inspector_brief(request: ExplanationGenerationRequest):
    """
    Generates enforcement briefing for field inspectors, including statutory exposures,
    mandatory registers to seize, and cross-examination checklists.
    """
    return ExplanationService.generate_inspector_explanation(
        establishment_id=request.establishment_id,
        worker_count=request.worker_count,
        wage_violation_count=request.wage_violation_count,
        ghost_worker_count=request.ghost_worker_count,
    )


@router.post("/employer-remediation", response_model=EmployerRemediationPlan)
def generate_employer_remediation(request: ExplanationGenerationRequest):
    """
    Generates constructive compliance remediation advisory for employers, detailing
    root cause analysis, wage differential arrears, and 14-day safe harbour cure steps.
    """
    return ExplanationService.generate_employer_remediation_plan(
        establishment_id=request.establishment_id,
        worker_count=request.worker_count,
        wage_violation_count=request.wage_violation_count,
        ghost_worker_count=request.ghost_worker_count,
    )
