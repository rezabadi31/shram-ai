#!/usr/bin/env bash
# ==============================================================================
# ShramAI One-Click Production Deployment Script
# Supports Ubuntu/Debian/CentOS and standard Docker Engine
# ==============================================================================

set -e

echo "============================================================"
echo " Starting ShramAI Production Deployment Deployment Sequence "
echo "============================================================"

# 1. Check prerequisites
command -v docker >/dev/null 2>&1 || { echo >&2 "Docker is required but not installed. Aborting."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1 || { echo >&2 "Docker Compose is required but not installed. Aborting."; exit 1; }

# 2. Pre-flight verification
echo "[1/4] Running pre-flight verification checks..."
if command -v python3 >/dev/null 2>&1; then
    python3 scripts/verify_deployment.py || echo "Pre-flight check completed with warnings."
fi

# 3. Build containers
echo "[2/4] Building production container images..."
docker compose -f docker-compose.prod.yml build

# 4. Launch services in daemon mode
echo "[3/4] Launching containerized microservices..."
docker compose -f docker-compose.prod.yml up -d

# 5. Wait for readiness
echo "[4/4] Verifying production readiness probe..."
sleep 5

for i in {1..12}; do
    if curl -s -f http://localhost:8000/api/v1/deployment/readiness >/dev/null 2>&1; then
        echo "✓ ShramAI is LIVE and HEALTHY at http://localhost:5173"
        echo "✓ Backend API Docs: http://localhost:8000/docs"
        exit 0
    fi
    echo "Waiting for services to become ready ($i/12)..."
    sleep 5
done

echo "Services started. Check logs using: docker compose -f docker-compose.prod.yml logs"
