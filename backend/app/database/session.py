"""Async SQLAlchemy engine, transaction, and request-session lifecycle."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings

logger = structlog.get_logger(__name__)
_engine: AsyncEngine | None = None
_AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    """Declarative base for future ORM models."""


def init_db(database_url: str | None = None) -> None:
    """Create the engine without opening a connection."""
    global _engine, _AsyncSessionLocal
    url = database_url if database_url is not None else settings.DATABASE_URL
    if not url:
        logger.info("database_disabled")
        return
    if _engine is not None:
        return
    _engine = create_async_engine(
        url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_recycle=settings.DB_POOL_RECYCLE,
    )
    _AsyncSessionLocal = async_sessionmaker(_engine, expire_on_commit=False)


async def check_db() -> bool:
    """Return whether the configured database accepts a trivial query."""
    if _AsyncSessionLocal is None:
        return False
    try:
        async with _AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning("database_health_check_failed", exception=str(exc))
        return False


async def close_db() -> None:
    """Dispose all pooled connections and reset module state."""
    global _engine, _AsyncSessionLocal
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _AsyncSessionLocal = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield one transactional session and always close it."""
    if _AsyncSessionLocal is None:
        raise RuntimeError("Database is not configured")
    async with _AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
