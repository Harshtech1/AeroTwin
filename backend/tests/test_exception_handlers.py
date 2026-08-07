"""Tests for global exception handlers and failure envelopes."""

from fastapi.testclient import TestClient


def test_404_returns_error_envelope(client: TestClient) -> None:
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"] == {"code": "HTTP_ERROR", "message": "Not Found"}
    assert body["meta"]["request_id"] == response.headers["x-request-id"]


def test_error_response_does_not_leak_details(client: TestClient) -> None:
    response = client.get("/not-present")
    body = response.json()
    assert "traceback" not in str(body).lower()
    assert isinstance(body["error"]["message"], str)
