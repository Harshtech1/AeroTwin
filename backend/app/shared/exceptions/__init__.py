"""Shared exception hierarchy for AeroTwin."""

from app.shared.exceptions.base import (
    AeroTwinError,
    AuthorizationError,
    BaseException,
    ConflictError,
    ConflictException,
    DatabaseError,
    DatabaseException,
    ExternalServiceError,
    ExternalServiceException,
    NotFoundError,
    NotFoundException,
    ServiceUnavailableError,
    ValidationError,
    ValidationException,
)

__all__ = [
    "AeroTwinError",
    "BaseException",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "AuthorizationError",
    "ServiceUnavailableError",
    "DatabaseError",
    "ExternalServiceError",
    "DatabaseException",
    "ExternalServiceException",
    "ValidationException",
    "NotFoundException",
    "ConflictException",
]
