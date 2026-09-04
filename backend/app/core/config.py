from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ShramAI — Labour Compliance & Inspection Intelligence"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "shram-ai-development-secret-key-32bytes-min"
    JWT_SECRET: Union[str, None] = None

    def model_post_init(self, __context) -> None:
        if self.JWT_SECRET:
            self.SECRET_KEY = self.JWT_SECRET
        import os
        if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
            if not self.UPLOAD_DIR.startswith("/tmp"):
                self.UPLOAD_DIR = "/tmp/data/raw"
            if not self.PROCESSED_DIR.startswith("/tmp"):
                self.PROCESSED_DIR = "/tmp/data/processed"
            try:
                os.makedirs(self.UPLOAD_DIR, exist_ok=True)
                os.makedirs(self.PROCESSED_DIR, exist_ok=True)
            except Exception:
                pass

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./shram.db"  # Fallback for lightweight local dev without Postgres running
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "shram_db"

    # Redis (Optional in MVP)
    REDIS_URL: str = "redis://localhost:6379/0"

    # External AI / OCR / Embedding APIs (optional, server-side only)
    LLM_API_KEY: Union[str, None] = None
    OCR_API_KEY: Union[str, None] = None
    EMBEDDING_API_KEY: Union[str, None] = None

    # CORS & Production Frontend Binding
    FRONTEND_URL: Union[str, None] = None
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        origins = []
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    origins = json.loads(v)
                except Exception:
                    origins = [i.strip() for i in v.strip("[]").replace('"', "").split(",") if i.strip()]
            else:
                origins = [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            origins = list(v)

        defaults = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
        for d in defaults:
            if d not in origins:
                origins.append(d)
        return origins

    # Storage paths
    UPLOAD_DIR: str = "./data/raw"
    PROCESSED_DIR: str = "./data/processed"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
