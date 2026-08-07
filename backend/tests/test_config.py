"""Configuration precedence and safety validation tests."""

import pytest
from app.config.settings import Settings
from pydantic import ValidationError


def test_explicit_settings_override_yaml() -> None:
    configured = Settings(ENVIRONMENT="testing", PROJECT_NAME="Override")
    assert configured.PROJECT_NAME == "Override"
    assert not configured.DATABASE_URL


def test_api_prefix_is_validated() -> None:
    with pytest.raises(ValidationError, match="API_V1_STR"):
        Settings(ENVIRONMENT="testing", API_V1_STR="api/v2")


def test_production_rejects_debug() -> None:
    with pytest.raises(ValidationError, match="DEBUG must be false"):
        Settings(
            ENVIRONMENT="production",
            DEBUG=True,
            BACKEND_CORS_ORIGINS=["https://aerotwin.example.com"],
        )


def test_production_rejects_wildcard_cors() -> None:
    with pytest.raises(ValidationError, match="Wildcard CORS"):
        Settings(ENVIRONMENT="production", DEBUG=False, BACKEND_CORS_ORIGINS=["*"])
