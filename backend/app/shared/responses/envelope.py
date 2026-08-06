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


class SuccessResponse[T](BaseModel):
    """Envelope for successful API responses."""

    success: bool = True
    data: T | None = None
    message: str | None = None
    request_id: str | None = None


class ErrorResponse(BaseModel):
    """Envelope for error API responses."""

    success: bool = False
    error: ErrorDetail
    request_id: str | None = None


def success(
    data: Any = None,
    message: str | None = None,
    request_id: str | None = None,
) -> dict:
    """Build a standardized success response dict."""
    return SuccessResponse(
        data=data, message=message, request_id=request_id
    ).model_dump(exclude_none=True)


def error(
    code: str,
    message: str,
    details: Any = None,
    request_id: str | None = None,
) -> dict:
    """Build a standardized error response dict."""
    return ErrorResponse(
        error=ErrorDetail(code=code, message=message, details=details),
        request_id=request_id,
    ).model_dump(exclude_none=True)
