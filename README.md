# ShramAI

### AI-Powered Labour Compliance & Inspection Intelligence

> **Transform labour documents into evidence-backed compliance insights, risk intelligence, and inspection priorities.**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)]()
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript%20%7C%20Vite-61dafb.svg)]()
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20pgvector-336791.svg)]()
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)]()
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)]()

---

## 🏛️ Deployment Architecture

ShramAI supports **two production deployment models**:

### Model A: 100% Unified Vercel Deployment (Recommended for Instant 1-Click Hosting)
Everything (React Frontend + FastAPI Backend Serverless Function) is hosted under a **single Vercel project and single domain** with zero CORS configuration required:

```text
                           PUBLIC INTERNET
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      VERCEL PROJECT     │
                    │  (https://shram-ai.com) │
                    ├────────────┬────────────┤
                    │  Frontend  │ Python API │
                    │   (Vite)   │ (FastAPI)  │
                    │  /(.*)     │ /api/(.*)  │
                    └────────────┴────────────┘
```

### Model B: Hybrid Architecture (Vercel Frontend + Render Backend)
Frontend on Vercel and long-running stateful FastAPI backend + PostgreSQL on Render:

```text
     VERCEL (React Frontend)  ──────HTTPS API──────►  RENDER (FastAPI Backend + Postgres)
```

---

## ⚡ 1-Click Unified Vercel Deployment (Deploy Everything on Vercel)

Deploy both the React frontend and FastAPI backend together on Vercel in under 2 minutes:

1. **Sign in to Vercel** ([vercel.com](https://vercel.com)).
2. Click **Add New...** > **Project**.
3. Select your GitHub repository: `rezabadi31/ShramAI`.
4. Leave **Root Directory** as `./` (Repository root — do not select a subfolder).
5. Vercel will automatically detect the settings configured in `vercel.json`:
   - **Build Command**: `npm --prefix frontend run build`
   - **Output Directory**: `frontend/dist`
   - **Serverless Function**: `api/index.py` (FastAPI backend)
6. *(Optional)* Add Environment Variables in Vercel:
   - `SECRET_KEY`: Enter any random 32+ character string (or let default development key run for demo).
   - `DATABASE_URL`: *(Optional)* Neon / Supabase / Render Postgres URL. If omitted, uses fast serverless fallback automatically.
7. Click **Deploy**.
8. **Done!** Your full-stack ShramAI application will be live at:  
   `https://your-shram-project.vercel.app`  
   - UI: `https://your-shram-project.vercel.app`  
   - API Docs: `https://your-shram-project.vercel.app/docs`  
   - Health Probe: `https://your-shram-project.vercel.app/health`

---

## 🚀 Alternative Hybrid Deployment Guide (Render + Vercel)

### Part 1: Backend Deployment on Render

1. **Sign in to Render** ([render.com](https://render.com)).
2. **Deploy with Blueprint (Recommended)**:
   - Go to **Blueprints** > **New Blueprint Instance**.
   - Connect repository: `shram-project` (or your GitHub fork).
   - Render will detect `render.yaml` and create:
     - `shram-backend` (Web Service on Free Plan)
     - `shram-postgres` (PostgreSQL Database on Free Plan)
3. **Or Deploy as Standalone Web Service**:
   - Create a new **Web Service** on Render connected to `shram-project`.
   - **Root Directory**: Leave empty or set to repository root.
   - **Environment**: `Python`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
4. **Configure Environment Variables in Render**:
   | Variable | Value | Description |
   | :--- | :--- | :--- |
   | `PYTHON_VERSION` | `3.11.9` | Required Python runtime |
   | `ENVIRONMENT` | `production` | Production environment mode |
   | `SECRET_KEY` | *(Render auto-generates or enter 32+ char key)* | JWT secret key |
   | `DATABASE_URL` | *(Postgres connection string)* | Render Postgres URL |
   | `FRONTEND_URL` | `https://your-shram-app.vercel.app` | Vercel domain for CORS |
5. **Copy Backend URL**: Note your public Render URL (e.g. `https://shram-backend.onrender.com`).

---

### Part 2: Frontend-Only Deployment on Vercel (Hybrid Model)

1. **Sign in to Vercel** ([vercel.com](https://vercel.com)).
2. **Import Git Repository**: Select `shram-project`.
3. **Configure Project Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend` *(Click Edit and select `frontend`)*
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
4. **Environment Variables**:
   | Variable | Value |
   | :--- | :--- |
   | `VITE_API_BASE_URL` | `https://your-shram-backend.onrender.com` *(Your Render URL without trailing slash)* |
5. **Click Deploy**. Vercel will build and assign a domain (e.g. `https://shram-ai.vercel.app`).
6. **Update Render Backend CORS**: Add your final Vercel domain to `FRONTEND_URL` in your Render Web Service environment variables.

---

## 💻 Local Development

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows:
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/health`

### 2. Frontend Setup
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
- Open UI: `http://localhost:5173`

---

## 🔐 Authentication & Roles

ShramAI uses JWT bearer authentication with strict role-based access control:
- **Employer (`role: EMPLOYER`)**:
  - Employer Login -> Employer Dashboard
  - Restricted to own establishment data, uploaded registers, compliance self-audit.
  - Denied access to Inspector Queue, Risk Ranking, and other establishments (HTTP 403).
- **Inspector (`role: INSPECTOR`)**:
  - Inspector Login -> Inspector Dashboard & Queue
  - Access to prioritized risk ranking, SHAP explainability, evidence cross-validation.
  - Authorized human-in-the-loop review.

---

## 🔍 Health Check & Diagnostics

The backend provides two public health endpoints for uptime monitoring:
- `GET /health`: Lightweight endpoint returning service status, version, and environment.
  ```json
  {
    "status": "healthy",
    "service": "ShramAI API",
    "version": "0.1.0",
    "environment": "production"
  }
  ```
- `GET /api/v1/health`: Detailed subsystem health probe verifying database connectivity, storage, and models.

---

## 🛡️ Security & Environment Best Practices

1. **No Frontend Secrets**: Only `VITE_API_BASE_URL` is exposed in the frontend. All LLM keys, database credentials, and JWT secrets remain strictly server-side.
2. **PostgreSQL Protocol Translation**: Handles Render's `postgres://` or `postgresql://` connection strings automatically and converts them to async `postgresql+asyncpg://`.
3. **CORS Hardening**: Wildcard origins are restricted in production; backend dynamically validates against `FRONTEND_URL` and `*.vercel.app`.
4. **Git Protection**: All `.env`, `.env.local`, `.venv`, and `node_modules` are excluded from Git via `.gitignore`.

---

## ❓ Troubleshooting

| Issue | Cause | Resolution |
| :--- | :--- | :--- |
| **Direct URL refresh gives 404 on Vercel** | SPA routing not rewritten | Verified `frontend/vercel.json` rewrites all traffic `/(.*)` to `/index.html`. |
| **CORS errors when frontend calls backend** | Render backend doesn't know Vercel domain | Set `FRONTEND_URL=https://your-app.vercel.app` in Render settings. Regex `*.vercel.app` is also auto-allowed. |
| **Render backend cold start delay** | Free tier spins down after inactivity | Wait ~30-50s on initial load; subsequent API requests respond immediately. |
| **Database connection error on Render** | Missing `postgresql+asyncpg://` driver prefix | `backend/app/database/session.py` auto-converts Render URLs to async driver format. |

