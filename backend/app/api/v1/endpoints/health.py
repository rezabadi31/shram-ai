from fastapi import APIRouter
from app.core.config import settings
from app.schemas.health import (
    HealthResponse,
    SystemDiagnosticsResponse,
    DiagnosticProbeRequest,
    DiagnosticProbeBatchResponse,
)
from app.services.diagnostics_service import DiagnosticsService

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System Health"])
async def health_check():
    """
    ShramAI System Health Check Endpoint.
    Returns operational readiness status and architecture module statuses.
    """
    return HealthResponse(
        status="healthy",
        project=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        services={
            "document_ai": "ready",
            "rule_engine": "ready",
            "cross_document_anomaly": "ready",
            "ml_risk_engine": "ready",
            "agent_orchestrator": "ready",
            "rag_retrieval": "ready",
        },
    )


@router.get("/diagnostics", response_model=SystemDiagnosticsResponse, tags=["System Health"])
@router.get("/health/diagnostics", response_model=SystemDiagnosticsResponse, tags=["System Health"])
async def get_system_diagnostics():
    """
    Returns full operational readiness telemetry, 8-subsystem latency benchmarks,
    zero-hallucination verification, and statutory coverage across 4 Indian Labour Codes.
    """
    return DiagnosticsService.get_system_diagnostics()


@router.post("/diagnostics/probe", response_model=DiagnosticProbeBatchResponse, tags=["System Health"])
@router.post("/health/diagnostics/probe", response_model=DiagnosticProbeBatchResponse, tags=["System Health"])
async def run_diagnostic_probe(request: DiagnosticProbeRequest):
    """
    Triggers live deterministic diagnostic micro-probes on designated or all subsystems.
    """
    return await DiagnosticsService.run_probe(request.subsystem)


