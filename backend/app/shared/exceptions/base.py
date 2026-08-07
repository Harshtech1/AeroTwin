"""
Base exception classes for AeroTwin.

All application-specific exceptions should inherit from AeroTwinError.
This allows consistent handling in the global exception handler middleware.
"""

from typing import Any


class AeroTwinError(Exception):
    """Root exception for all AeroTwin application errors."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        message: str | None = None,
        error_code: str | None = None,
        details: Any | None = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.error_code = error_code or self.__class__.error_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AeroTwinError):
    """Raised when a requested resource does not exist."""

    status_code = 404
    error_code = "NOT_FOUND"
    message = "The requested resource was not found."


class ValidationError(AeroTwinError):
    """Raised when input data fails business-level validation."""

    status_code = 422
    error_code = "VALIDATION_ERROR"
    message = "The provided data is invalid."


class ConflictError(AeroTwinError):
    """Raised when an operation conflicts with the current state."""

    status_code = 409
    error_code = "CONFLICT"
    message = "A conflict occurred with the current state of the resource."


class AuthorizationError(AeroTwinError):
    """Raised when an action is not permitted."""

    status_code = 403
    error_code = "FORBIDDEN"
    message = "You do not have permission to perform this action."


class ServiceUnavailableError(AeroTwinError):
    """Raised when a downstream service is unavailable."""

    status_code = 503
    error_code = "SERVICE_UNAVAILABLE"
    message = "A required service is temporarily unavailable."


class DatabaseError(AeroTwinError):
    """Raised when a persistence operation fails."""

    status_code = 503
    error_code = "DATABASE_ERROR"
    message = "The database operation could not be completed."


class ExternalServiceError(AeroTwinError):
    """Raised when communication with an external dependency fails."""

    status_code = 502
    error_code = "EXTERNAL_SERVICE_ERROR"
    message = "An external service operation failed."


# Explicit exception names requested by the public infrastructure contract.
BaseException = AeroTwinError
ValidationException = ValidationError
NotFoundException = NotFoundError
ConflictException = ConflictError
DatabaseException = DatabaseError
ExternalServiceException = ExternalServiceError
