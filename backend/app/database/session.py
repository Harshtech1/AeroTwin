"""
Async database session management for AeroTwin.

Design: engine and session factory are module-level variables initialised
by init_db() rather than at import time. This:
  - Prevents accidental DB connections during import / testing.
  - Allows test suites to call init_db() with a lightweight test URL.
  - Keeps the lifespan handler as the single source of DB initialisation.

Usage:
    # In main.py lifespan (startup):
    from app.database.session import init_db
    await init_db()

    # In FastAPI dependencies:
    from app.database.session import get_db
    async def some_endpoint(db: AsyncSession = Depends(get_db)): ...
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings

# ---------------------------------------------------------------------------
# Module-level state — initialised lazily by init_db()
# ---------------------------------------------------------------------------
_engine = None
_AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy ORM models."""

    pass


async def init_db() -> None:
    """
    Initialise the async engine and session factory.

    Called once during the application lifespan startup.
    Skipped safely when DATABASE_URL is not configured (e.g., during tests
    that do not require a real database).
    """
    global _engine, _AsyncSessionLocal

    if not settings.DATABASE_URL:
        return

    _engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    _AsyncSessionLocal = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Verify connectivity by running a lightweight query.
    try:
        async with _AsyncSessionLocal() as session:
            from sqlalchemy import text

            await session.execute(text("SELECT 1"))
    except Exception:
        pass  # Non-critical at startup; service can degrade gracefully.


async def close_db() -> None:
    """Dispose the engine connection pool on application shutdown."""
    if _engine is not None:
        await _engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an AsyncSession per request.

    Raises:
        RuntimeError: If init_db() has not been called or DATABASE_URL is
            not configured.
    """
    if _AsyncSessionLocal is None:
        raise RuntimeError(
            "Database is not initialised. "
            "Ensure init_db() is called during application startup and "
            "that DATABASE_URL is configured."
        )
    async with _AsyncSessionLocal() as session:
        yield session
