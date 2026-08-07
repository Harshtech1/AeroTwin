"""
Standardized API response envelope for AeroTwin.

All API responses are wrapped in a consistent structure:

Success:
    {
        "success": true,
        "data": <payload>,
        "message": "Optional human-readable message",
        "request_id": "uuid"
    }

Error:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Human-readable error message",
            "details": <optional extra context>
        },
        "request_id": "uuid"
    }
"""

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Structured error information embedded in error responses."""

    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error description.")
    details: Any | None = Field(None, description="Optional additional context.")


class ResponseMeta(BaseModel):
    """Optional response metadata used for tracing and pagination."""

    request_id: str | None = None
    page: int | None = None
    page_size: int | None = None
    total: int | None = None
    total_pages: int | None = None


class PaginationParams(BaseModel):
    """Validated offset pagination input shared by list endpoints."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class SuccessResponse[T](BaseModel):
    """Envelope for successful API responses."""

    success: bool = True
    data: T | None = None
    meta: ResponseMeta | None = None


class ErrorResponse(BaseModel):
    """Envelope for error API responses."""

    success: bool = False
    error: ErrorDetail
    meta: ResponseMeta | None = None


def success(
    data: Any = None,
    message: str | None = None,
    request_id: str | None = None,
    meta: ResponseMeta | None = None,
) -> dict[str, Any]:
    """Build a standardized success response dict."""
    del message  # Kept as a compatibility parameter during envelope migration.
    response_meta = meta or (
        ResponseMeta(request_id=request_id) if request_id else None
    )
    return SuccessResponse(data=data, meta=response_meta).model_dump(exclude_none=True)


def error(
    code: str,
    message: str,
    details: Any = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Build a standardized error response dict."""
    return ErrorResponse(
        error=ErrorDetail(code=code, message=message, details=details),
        meta=ResponseMeta(request_id=request_id) if request_id else None,
    ).model_dump(exclude_none=True)
