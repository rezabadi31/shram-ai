"""
Database connection and session handling.
Supports async engines for both PostgreSQL and SQLite fallback.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

Base = declarative_base()


def get_async_database_url(raw_url: str) -> str:
    """
    Normalizes PostgreSQL connection string for async SQLAlchemy engine.
    Render and Cloud PaaS providers provide 'postgres://' or 'postgresql://' by default.
    Also handles ephemeral /tmp path when running SQLite in serverless environments (Vercel).
    """
    import os
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        if "shram.db" in raw_url and "/tmp" not in raw_url:
            raw_url = raw_url.replace("./shram.db", "/tmp/shram.db").replace("shram.db", "/tmp/shram.db")

    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+asyncpg://", 1)
    if raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+asyncpg://"):
        return raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return raw_url


# Engine creation
engine = create_async_engine(
    get_async_database_url(settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for obtaining database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
