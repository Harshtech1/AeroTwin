"""
AeroTwin FastAPI application entry point.

Sprint 2: Backend Infrastructure
---------------------------------
- Lifespan context manager (startup / shutdown hooks)
- Structured logging initialisation
- Database initialisation and teardown
- CORS middleware
- Request ID middleware
- Global exception handlers
- OpenAPI metadata
- Versioned API routing
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routers import api_router
from app.api.v1.endpoints import health
from app.config.settings import settings
from app.constants.application import DESCRIPTION, PROJECT_NAME, VERSION
from app.core.logging import setup_logging
from app.database.session import close_db, init_db
from app.middleware.exception_handler import (
    aerotwin_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.middleware.observability import ObservabilityMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.shared.exceptions.base import AeroTwinError
from app.shared.responses.envelope import success

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup tasks → yield → teardown."""
    # ── Startup ──────────────────────────────────────────────────────────────
    setup_logging()
    logger.info(
        "AeroTwin starting",
        version=VERSION,
        environment=settings.ENVIRONMENT,
        debug=settings.DEBUG,
    )
    init_db()

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    await close_db()
    logger.info("AeroTwin shutting down")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app() -> FastAPI:
    """Construct and return the configured FastAPI application."""
    app = FastAPI(
        title=PROJECT_NAME,
        description=DESCRIPTION,
        version=settings.VERSION,
        # Only expose OpenAPI docs in non-production environments.
        openapi_url=(
            f"{settings.API_V1_STR}/openapi.json"
            if settings.ENVIRONMENT != "production"
            else None
        ),
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MINIMUM_SIZE)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(ObservabilityMiddleware)

    # ── Request ID (registered after CORS, before route handlers) ────────────
    app.add_middleware(RequestIDMiddleware)

    # ── Exception handlers ────────────────────────────────────────────────────
    app.add_exception_handler(AeroTwinError, aerotwin_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)  # type: ignore[arg-type]

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(health.router)

    # ── Root endpoint (framework-level liveness probe, not versioned) ─────────
    @app.get("/", tags=["root"], include_in_schema=False)
    async def root() -> dict[str, object]:
        return success(
            {"project": PROJECT_NAME, "status": "running", "version": settings.VERSION}
        )

    return app


app = create_app()
