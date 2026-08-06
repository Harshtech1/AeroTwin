"""
Request ID middleware for AeroTwin.

Generates a unique UUID for every incoming request and:
  1. Binds it to the structlog context so all log lines for the request
     carry request_id automatically.
  2. Stores it in request.state.request_id for endpoint access.
  3. Attaches it as an X-Request-ID response header.

If the client sends an X-Request-ID header, that value is used instead
of generating a new one (useful for request tracing across services).
"""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.constants.api import HEADER_REQUEST_ID

logger = structlog.get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to every request/response cycle."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Honour client-supplied request ID or generate a fresh one.
        request_id = request.headers.get(HEADER_REQUEST_ID) or str(uuid.uuid4())

        # Expose on request state for endpoint access.
        request.state.request_id = request_id

        # Bind to structlog context vars so every log line in this request
        # automatically carries request_id.
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        response: Response = await call_next(request)

        # Propagate the request ID back to the caller.
        response.headers[HEADER_REQUEST_ID] = request_id
        return response
