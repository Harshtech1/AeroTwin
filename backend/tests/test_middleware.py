"""Request context, security, compression, and CORS middleware tests."""

import uuid

from fastapi.testclient import TestClient


def test_request_id_generated_as_uuid(client: TestClient) -> None:
    response = client.get("/")
    uuid.UUID(response.headers["x-request-id"])


def test_request_id_honours_client_value(client: TestClient) -> None:
    response = client.get("/", headers={"X-Request-ID": "upstream-id"})
    assert response.headers["x-request-id"] == "upstream-id"


def test_request_id_unique_per_request(client: TestClient) -> None:
    assert (
        client.get("/").headers["x-request-id"]
        != client.get("/").headers["x-request-id"]
    )


def test_cors_preflight(client: TestClient) -> None:
    response = client.options(
        "/",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers["access-control-allow-origin"] == "https://example.com"


def test_security_headers(client: TestClient) -> None:
    response = client.get("/")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "default-src 'none'" in response.headers["content-security-policy"]


def test_request_id_on_error_response(client: TestClient) -> None:
    response = client.get("/nonexistent-route-12345")
    assert response.status_code == 404
    assert response.headers["x-request-id"]
