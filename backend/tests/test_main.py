"""Application metadata and operational endpoint tests."""

from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["data"] == {
        "project": "AeroTwin",
        "status": "running",
        "version": "0.1.0",
    }


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "healthy"
    assert body["data"]["environment"] == "testing"
    assert body["data"]["dependencies"]["database"] == "disabled"
    assert body["meta"]["request_id"] == response.headers["x-request-id"]


def test_liveness_does_not_require_dependencies(client: TestClient) -> None:
    response = client.get("/liveness")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "alive"


def test_readiness_succeeds_when_database_disabled(client: TestClient) -> None:
    response = client.get("/readiness")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ready"


def test_openapi_metadata_and_versioning(client: TestClient) -> None:
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "AeroTwin"
    assert "/api/v1/health" in schema["paths"]


def test_health_honours_client_request_id(client: TestClient) -> None:
    custom_id = "test-request-id-12345"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.headers["x-request-id"] == custom_id
    assert response.json()["meta"]["request_id"] == custom_id
