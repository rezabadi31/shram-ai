from fastapi import APIRouter, Response, status
from app.schemas.deployment import (
    DeploymentStatusResponse,
    ReadinessProbeResponse,
    LivenessProbeResponse,
)
from app.services.deployment_service import DeploymentService

router = APIRouter()


@router.get("/status", response_model=DeploymentStatusResponse, tags=["Deployment & Operations"])
async def get_deployment_status():
    """
    Returns full deployment operational status, container runtime, environment configuration,
    and feature flags for ShramAI.
    """
    return DeploymentService.get_deployment_status()


@router.get("/readiness", response_model=ReadinessProbeResponse, tags=["Deployment & Operations"])
async def get_readiness_probe(response: Response):
    """
    Kubernetes Readiness Probe. Returns HTTP 200 when ready to accept user requests,
    or HTTP 503 Service Unavailable if any critical subsystem is unhealthy.
    """
    probe = DeploymentService.check_readiness()
    if not probe.all_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return probe


@router.get("/liveness", response_model=LivenessProbeResponse, tags=["Deployment & Operations"])
async def get_liveness_probe():
    """
    Kubernetes Liveness Probe. Returns HTTP 200 confirming the server process is responsive.
    """
    return DeploymentService.check_liveness()
