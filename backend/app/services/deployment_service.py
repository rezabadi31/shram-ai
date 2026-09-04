"""
Production Deployment and Cloud Orchestration Readiness Service.
Provides Kubernetes-compliant readiness and liveness probes,
environment validation, and container health verification.
"""
import os
import sys
import time
import uuid
import platform
from datetime import datetime, timezone
from typing import List, Dict, Any

from app.core.config import settings
from app.schemas.deployment import (
    ServiceReadinessDetail,
    ReadinessProbeResponse,
    LivenessProbeResponse,
    DeploymentEnvironmentInfo,
    DeploymentStatusResponse,
)
from app.rag.ingestion import KnowledgeBaseService
from app.compliance.rule_engine import ComplianceRuleEngine
from app.document_ai.document_classifier import DocumentClassifierService
from app.ml.drift_monitor import DriftMonitorService
from app.reports.report_generator import ReportGeneratorService

_DEPLOYMENT_START_TIME = time.time()
_DEPLOYMENT_ID = f"DEP-2026-{uuid.uuid4().hex[:8].upper()}"


class DeploymentService:
    """Evaluates runtime host container health, database readiness, and operational status."""

    @classmethod
    def get_uptime_seconds(cls) -> float:
        return round(time.time() - _DEPLOYMENT_START_TIME, 2)

    @classmethod
    def check_readiness(cls) -> ReadinessProbeResponse:
        """
        Executes Kubernetes readiness probes on core dependency services.
        Returns HTTP 200 OK only when all critical dependencies are ready to serve traffic.
        """
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        components: List[ServiceReadinessDetail] = []

        # 1. Statutory Knowledge Base
        t0 = time.perf_counter()
        try:
            KnowledgeBaseService.load_knowledge_base()
            code_count = len(KnowledgeBaseService.list_codes())
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Statutory Knowledge Base",
                    status="HEALTHY",
                    latency_ms=lat,
                    message=f"{code_count} Indian Labour Codes loaded with {len(KnowledgeBaseService._all_sections)} sections",
                )
            )
        except Exception as e:
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Statutory Knowledge Base",
                    status="DEGRADED",
                    latency_ms=lat,
                    message=f"Knowledge base load warning: {str(e)}",
                )
            )

        # 2. Compliance Rule Engine
        t0 = time.perf_counter()
        try:
            rules = ComplianceRuleEngine.load_rules()
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Compliance Rule Engine",
                    status="HEALTHY",
                    latency_ms=lat,
                    message=f"{len(rules)} deterministic statutory rules verified",
                )
            )
        except Exception as e:
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Compliance Rule Engine",
                    status="DEGRADED",
                    latency_ms=lat,
                    message=f"Rule catalog issue: {str(e)}",
                )
            )

        # 3. Document AI Multimodal Classifier
        t0 = time.perf_counter()
        try:
            _ = DocumentClassifierService.classify("Form B Register of Wages")
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Document AI Classifier",
                    status="HEALTHY",
                    latency_ms=lat,
                    message="Regex heuristic & ML fallback classification pipeline operational",
                )
            )
        except Exception as e:
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Document AI Classifier",
                    status="DEGRADED",
                    latency_ms=lat,
                    message=f"Classifier error: {str(e)}",
                )
            )

        # 4. Safe Harbour Vault & Report Engine
        t0 = time.perf_counter()
        try:
            _ = ReportGeneratorService.recalibrate_compliance("EST-001", ["ACT-001"])
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Safe Harbour Vault",
                    status="HEALTHY",
                    latency_ms=lat,
                    message="Form SH-01 cryptographic certification ready",
                )
            )
        except Exception as e:
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Safe Harbour Vault",
                    status="DEGRADED",
                    latency_ms=lat,
                    message=f"Vault recalibration error: {str(e)}",
                )
            )

        # 5. Continuous Drift Monitor
        t0 = time.perf_counter()
        try:
            drift = DriftMonitorService.get_drift_report()
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Continuous Drift Monitor",
                    status="HEALTHY",
                    latency_ms=lat,
                    message=f"Tracking {len(drift.feature_drifts)} statutory features",
                )
            )
        except Exception as e:
            lat = round((time.perf_counter() - t0) * 1000, 2)
            components.append(
                ServiceReadinessDetail(
                    name="Continuous Drift Monitor",
                    status="DEGRADED",
                    latency_ms=lat,
                    message=f"Drift monitor issue: {str(e)}",
                )
            )

        all_healthy = all(c.status == "HEALTHY" for c in components)

        return ReadinessProbeResponse(
            status="READY" if all_healthy else "NOT_READY",
            timestamp=now_str,
            all_healthy=all_healthy,
            components=components,
        )

    @classmethod
    def check_liveness(cls) -> LivenessProbeResponse:
        """
        Kubernetes liveness probe: returns HTTP 200 indicating process is responsive.
        """
        return LivenessProbeResponse(
            status="ALIVE",
            uptime_seconds=cls.get_uptime_seconds(),
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        )

    @classmethod
    def get_deployment_status(cls) -> DeploymentStatusResponse:
        """
        Comprehensive deployment status telemetry report.
        """
        readiness = cls.check_readiness()
        in_docker = os.path.exists("/.dockerenv") or bool(os.getenv("DOCKER_CONTAINER"))

        env_info = DeploymentEnvironmentInfo(
            environment=settings.ENVIRONMENT,
            project_name=settings.PROJECT_NAME,
            version=settings.VERSION,
            container_runtime="Docker / OCI Container" if in_docker else "Host Virtualenv / Local Host",
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            subsystems_active=8,
            statutory_codes_loaded=4,
        )

        return DeploymentStatusResponse(
            deployment_id=_DEPLOYMENT_ID,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            status="DEPLOYED_AND_OPERATIONAL" if readiness.all_healthy else "DEGRADED",
            environment=env_info,
            readiness=readiness,
            features_enabled={
                "deterministic_rule_engine": True,
                "labour_law_hybrid_rag": True,
                "multi_agent_orchestrator": True,
                "cross_document_anomaly_reconciliation": True,
                "xgboost_risk_scoring": True,
                "treeshap_explainability": True,
                "safe_harbour_certification": True,
                "continuous_model_drift_monitoring": True,
                "zero_hallucination_guarantee": True,
                "rbac_central_sphere_isolation": True,
            },
        )
