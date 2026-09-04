from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ServiceReadinessDetail(BaseModel):
    name: str
    status: str
    latency_ms: float
    message: str


class ReadinessProbeResponse(BaseModel):
    status: str = Field(..., description="READY or NOT_READY")
    timestamp: str
    all_healthy: bool
    components: List[ServiceReadinessDetail]


class LivenessProbeResponse(BaseModel):
    status: str = Field(..., description="ALIVE")
    uptime_seconds: float
    timestamp: str


class DeploymentEnvironmentInfo(BaseModel):
    environment: str
    project_name: str
    version: str
    container_runtime: str
    python_version: str
    subsystems_active: int
    statutory_codes_loaded: int


class DeploymentStatusResponse(BaseModel):
    deployment_id: str
    timestamp: str
    status: str
    environment: DeploymentEnvironmentInfo
    readiness: ReadinessProbeResponse
    features_enabled: Dict[str, bool]
