"""
Global exception handler for AeroTwin.

Catches all exceptions that propagate out of route handlers and formats
them as standardised ErrorResponse envelopes so the caller always receives
a consistent JSON structure regardless of error type.

Handlers are registered on the FastAPI application in main.py via
app.add_exception_handler().
"""

from __future__ import annotations

import structlog
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.exceptions.base import AeroTwinError
from app.shared.responses.envelope import error as make_error

logger = structlog.get_logger(__name__)


def _get_request_id(request: Request) -> str | None:
    """Safely retrieve request_id from request state."""
    return getattr(request.state, "request_id", None)


async def aerotwin_exception_handler(
    request: Request,
    exc: AeroTwinError,
) -> JSONResponse:
    """Handle all domain-level AeroTwinError subclasses."""
    request_id = _get_request_id(request)
    logger.warning(
        "Application error",
        error_code=exc.error_code,
        status_code=exc.status_code,
        message=exc.message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=make_error(
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
            request_id=request_id,
        ),
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Handle Starlette/FastAPI HTTP exceptions (e.g. 404 from routing)."""
    request_id = _get_request_id(request)
    logger.warning(
        "HTTP error",
        status_code=exc.status_code,
        detail=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=make_error(
            code="HTTP_ERROR",
            message=str(exc.detail),
            request_id=request_id,
        ),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle Pydantic request-body / query-param validation errors."""
    request_id = _get_request_id(request)
    logger.warning("Validation error", errors=exc.errors())
    return JSONResponse(
        status_code=422,
        content=make_error(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            details=exc.errors(),
            request_id=request_id,
        ),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Catch-all handler — prevents raw Python tracebacks leaking to callers."""
    request_id = _get_request_id(request)
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content=make_error(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
            request_id=request_id,
        ),
    )
