"""Shared exception hierarchy for AeroTwin."""

from app.shared.exceptions.base import (
    AeroTwinError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    ServiceUnavailableError,
    ValidationError,
)

__all__ = [
    "AeroTwinError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "AuthorizationError",
    "ServiceUnavailableError",
]
