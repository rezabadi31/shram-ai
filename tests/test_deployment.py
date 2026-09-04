import os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_deployment_status_endpoint():
    """
    Tests GET /api/v1/deployment/status.
    Verifies full deployment metadata, container runtime info, and feature flags.
    """
    response = client.get("/api/v1/deployment/status")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] in ("DEPLOYED_AND_OPERATIONAL", "READY")
    assert data["deployment_id"].startswith("DEP-2026-")
    assert "timestamp" in data

    env = data["environment"]
    assert "ShramAI" in env["project_name"]
    assert env["subsystems_active"] == 8
    assert env["statutory_codes_loaded"] == 4
    assert len(env["python_version"]) > 0

    features = data["features_enabled"]
    assert features["deterministic_rule_engine"] is True
    assert features["labour_law_hybrid_rag"] is True
    assert features["multi_agent_orchestrator"] is True
    assert features["zero_hallucination_guarantee"] is True
    assert features["safe_harbour_certification"] is True


def test_deployment_readiness_probe():
    """
    Tests GET /api/v1/deployment/readiness.
    Verifies Kubernetes readiness probe returns HTTP 200 and all components are HEALTHY.
    """
    response = client.get("/api/v1/deployment/readiness")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "READY"
    assert data["all_healthy"] is True
    assert len(data["components"]) >= 5

    comp_names = [c["name"] for c in data["components"]]
    assert "Statutory Knowledge Base" in comp_names
    assert "Compliance Rule Engine" in comp_names
    assert "Document AI Classifier" in comp_names
    assert "Safe Harbour Vault" in comp_names
    assert "Continuous Drift Monitor" in comp_names

    for comp in data["components"]:
        assert comp["status"] == "HEALTHY"
        assert comp["latency_ms"] >= 0.0


def test_deployment_liveness_probe():
    """
    Tests GET /api/v1/deployment/liveness.
    Verifies Kubernetes liveness probe returns HTTP 200 and positive uptime.
    """
    response = client.get("/api/v1/deployment/liveness")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ALIVE"
    assert data["uptime_seconds"] >= 0.0
    assert "timestamp" in data


def test_deployment_packaging_files_integrity():
    """
    Verifies that all Phase 30 production packaging and deployment configuration files exist.
    """
    root_dir = Path(__file__).resolve().parent.parent

    # Dockerfiles
    assert (root_dir / "backend" / "Dockerfile").exists()
    assert (root_dir / "frontend" / "Dockerfile").exists()
    assert (root_dir / "frontend" / "nginx.conf").exists()

    # Compose files
    assert (root_dir / "docker-compose.yml").exists()
    assert (root_dir / "docker-compose.prod.yml").exists()

    # CI/CD and PaaS Blueprints
    assert (root_dir / ".github" / "workflows" / "ci-cd.yml").exists()
    assert (root_dir / "render.yaml").exists()
    assert (root_dir / "railway.json").exists()

    # Scripts & Documentation
    assert (root_dir / "scripts" / "verify_deployment.py").exists()
    assert (root_dir / "scripts" / "deploy.sh").exists()
    assert (root_dir / "docs" / "DEPLOYMENT.md").exists()
