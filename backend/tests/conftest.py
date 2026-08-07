"""
Shared pytest fixtures for AeroTwin backend test suite.

The TestClient is module-scoped for efficiency. The ENVIRONMENT is forced
to 'testing' so the YamlConfigSettingsSource loads configs/testing.yaml.
DATABASE_URL is unset so init_db() is a no-op during tests that don't
need a real database.
"""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

# Force environment before any app module is imported.
os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("DATABASE_URL", "")  # Disable DB for unit tests


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Return a TestClient wrapping the AeroTwin application."""
    from app.main import app

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture
def anyio_backend() -> str:
    """Use asyncio for async database contract tests."""
    return "asyncio"
