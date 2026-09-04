"""
ShramAI: Agentic AI-Powered Smart Labour Compliance & Inspection Intelligence System
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=(
            "ShramAI is an India-specific, research-grade labour compliance intelligence "
            "prototype designed around proactive, evidence-backed, and human-supervised "
            "compliance and inspection intelligence under the Four Labour Codes of India."
        ),
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    cors_origins = list(settings.CORS_ORIGINS)
    if settings.FRONTEND_URL:
        clean_url = settings.FRONTEND_URL.strip().rstrip("/")
        if clean_url not in cors_origins:
            cors_origins.append(clean_url)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API Routers
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "project": settings.PROJECT_NAME,
            "status": "online",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health",
            "api_health": f"{settings.API_V1_PREFIX}/health",
        }

    @app.get("/health", tags=["Root"])
    async def root_health():
        """Public health check endpoint for cloud load balancers and deployment monitoring."""
        return {
            "status": "healthy",
            "service": "ShramAI API",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }

    return app


app = create_application()
