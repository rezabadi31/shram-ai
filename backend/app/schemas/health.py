from pydantic import BaseModel, Field
from typing import Dict, Any, List


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["healthy"])
    project: str = Field(..., examples=["ShramAI"])
    version: str = Field(..., examples=["0.1.0"])
    environment: str = Field(..., examples=["development"])
    services: Dict[str, Any] = Field(default_factory=dict)


class SubsystemMetric(BaseModel):
    name: str
    status: str
    latency_ms: float
    details: str


class StatutoryCoverageMetric(BaseModel):
    code_name: str
    statutory_sections_count: int
    rule_templates_count: int
    coverage_status: str


class SystemDiagnosticsResponse(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: float
    active_test_suite_passed: int
    active_test_suite_failed: int
    zero_hallucination_guarantee: bool
    rbac_enforcement_status: str
    model_version: str
    subsystems: List[SubsystemMetric]
    statutory_coverage: List[StatutoryCoverageMetric]


class DiagnosticProbeRequest(BaseModel):
    subsystem: str = Field(..., description="Target subsystem to probe or 'all'")


class DiagnosticProbeResult(BaseModel):
    subsystem: str
    status: str
    latency_ms: float
    output: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str


class DiagnosticProbeBatchResponse(BaseModel):
    total_probes: int
    all_passed: bool
    results: List[DiagnosticProbeResult]
    timestamp: str

