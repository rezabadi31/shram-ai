# ShramAI: Production Deployment & Operations Manual

**Phase 30: Enterprise Production Infrastructure, Cloud Packaging & CI/CD**

---

## 1. System Architecture Overview

ShramAI is architected as an asynchronous, modular containerized platform consisting of four core tiers:

```text
                                  Internet / End Users
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │      Nginx Reverse Proxy & Static Host       │
                    │           (Port 5173 / Port 80)              │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │            FastAPI Backend Engine            │
                    │        (Port 8000 - Non-root Appuser)        │
                    │   - 8 Architectural Subsystems               │
                    │   - 4 Indian Labour Codes Knowledge Base     │
                    │   - Deterministic Rule Engine                │
                    │   - XGBoost ML Risk & TreeSHAP               │
                    └───────────────┬──────────────┬───────────────┘
                                    │              │
                   ┌────────────────┴───┐     ┌────┴────────────────┐
                   │ PostgreSQL (pg16)  │     │   Redis (Cache &    │
                   │  + pgvector Vector │     │   Task Queue)       │
                   └────────────────────┘     └─────────────────────┘
```

---

## 2. Pre-Flight Verification

Before deploying, run the built-in diagnostic pre-flight script:

```bash
# In Windows / Local environment
backend\.venv\Scripts\python scripts/verify_deployment.py

# In Linux / macOS
python3 scripts/verify_deployment.py
```

Expected output:
```text
===============================================================
      ShramAI Production Deployment Verification Engine         
===============================================================

[PASS] Python Version: 3.11.x (Requires Python >= 3.10)
[PASS] Project Structure: All core directories verified
[PASS] Statutory Knowledge Base: All 4 Indian Labour Codes present
[PASS] Deterministic Rules: Statutory rules catalog present
[PASS] Docker Packaging: Production Dockerfiles & Compose profiles verified
[PASS] CI/CD Automation: GitHub Actions workflow verified
[PASS] Cloud Blueprints: Render & Railway manifests verified
[PASS] Backend Architecture: App factory & DeploymentService verified

Verification Results: 8/8 pre-flight checks passed.
✓ ShramAI is 100% READY FOR PRODUCTION DEPLOYMENT.
```

---

## 3. Deployment Options

### Option A: Local / Bare-Metal Docker Compose (Quickstart)

```bash
# 1. Clone repository
git clone https://github.com/rezabadi31/ShramAI.git
cd ShramAI

# 2. Build and launch all production microservices
docker compose -f docker-compose.prod.yml up -d --build

# 3. Verify logs
docker compose -f docker-compose.prod.yml logs -f

# 4. Access services
# Frontend UI:   http://localhost:5173
# Backend API:   http://localhost:8000/docs
# K8s Readiness: http://localhost:8000/api/v1/deployment/readiness
```

---

### Option B: Kubernetes (K8s) Deployment

ShramAI includes Kubernetes-compliant **Liveness** and **Readiness** probe contracts:

- **Readiness Probe**: `GET /api/v1/deployment/readiness`  
  *Returns `HTTP 200 OK` when statutory rules, knowledge base, models, and vault are initialized. Returns `HTTP 503` if any component fails.*
- **Liveness Probe**: `GET /api/v1/deployment/liveness`  
  *Returns `HTTP 200 OK` with process uptime to verify server health.*

Sample Kubernetes Deployment snippet:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shram-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: backend
        image: shramai/backend:v1.0
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /api/v1/deployment/readiness
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 15
        livenessProbe:
          httpGet:
            path: /api/v1/deployment/liveness
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 20
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
```

---

### Option C: AWS Cloud (ECS Fargate + RDS PostgreSQL)

1. **Database**: Provision Amazon RDS for PostgreSQL (PostgreSQL 16) with the `pgvector` extension enabled.
2. **Container Registry**: Push backend and frontend images to AWS ECR.
3. **Compute**: Deploy task definitions to AWS ECS using Fargate (serverless containers).
4. **Networking**: Configure an Application Load Balancer (ALB) with SSL/TLS certificate termination via AWS Certificate Manager.
5. **Environment Variables**: Store sensitive values (`SECRET_KEY`, `DATABASE_URL`) in AWS Systems Manager Parameter Store or Secrets Manager.

---

### Option D: Microsoft Azure (Azure Container Apps)

1. **Database**: Provision Azure Database for PostgreSQL Flexible Server.
2. **Container Apps**:
   ```bash
   az containerapp up \
     --name shram-backend \
     --resource-group rg-shram-prod \
     --location centralindia \
     --environment env-shram-prod \
     --target-port 8000 \
     --ingress external
   ```
3. Set environment variable `ENVIRONMENT=production`.

---

### Option E: Google Cloud Platform (Cloud Run + Cloud SQL)

1. **Database**: Provision Cloud SQL for PostgreSQL 16.
2. **Deploy Backend**:
   ```bash
   gcloud run deploy shram-backend \
     --image gcr.io/shram-ai/backend:latest \
     --platform managed \
     --region asia-south1 \
     --set-env-vars ENVIRONMENT=production
   ```
3. **Deploy Frontend**:
   ```bash
   gcloud run deploy shram-frontend \
     --image gcr.io/shram-ai/frontend:latest \
     --platform managed \
     --region asia-south1
   ```

---

### Option F: One-Click PaaS (Render / Railway)

The repository includes ready-to-use manifests:
- **Render**: Connect repository and select `render.yaml`. It automatically provisions the PostgreSQL database, Python backend web service, and static frontend site.
- **Railway**: Connect repository and select `railway.json`. Dockerfile builds and deploys automatically with healthcheck monitoring.

---

## 4. Production Security Hardening

1. **Non-Root Execution**:
   The backend container enforces non-root user execution (`UID 1001`, `shramuser`) adhering to CIS Docker Benchmarks.
2. **CORS Restrictions**:
   Configure allowed domains in `.env`:
   ```bash
   CORS_ORIGINS=["https://shram.gov.in", "https://compliance.shram.gov.in"]
   ```
3. **Security Headers**:
   Frontend Nginx automatically attaches `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `X-XSS-Protection`.

---

## 5. Automated CI/CD Workflows

Continuous Integration and Continuous Deployment is automated via GitHub Actions (`.github/workflows/ci-cd.yml`):
- **Unit & Integration Testing**: Executes all 129+ backend tests against mock and statutory datasets.
- **Frontend Validation**: Runs TypeScript compilation and Vite build.
- **Docker Verification**: Builds container images to guarantee deployment readiness on every commit to `main`.
