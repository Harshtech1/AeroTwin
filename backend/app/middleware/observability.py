"""Request logging, distributed tracing context, and timing middleware."""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

logger = structlog.get_logger(__name__)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Emit one structured completion event for every HTTP request."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        started = time.perf_counter()
        trace_id = request.headers.get("traceparent", "").split("-")[1:2]
        trace_id_value = trace_id[0] if trace_id else uuid.uuid4().hex
        request.state.trace_id = trace_id_value
        structlog.contextvars.bind_contextvars(
            trace_id=trace_id_value,
            endpoint=request.url.path,
        )
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as exc:
            logger.exception("request_failed", exception=str(exc))
            raise
        finally:
            duration_ms = round((time.perf_counter() - started) * 1000, 3)
            logger.info(
                "request_completed",
                status_code=status_code,
                duration_ms=duration_ms,
            )
