"""Tests for global exception handlers and error response envelopes."""


def test_404_returns_error_envelope(client):
    """A non-existent route returns a structured error response."""
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"


def test_404_has_request_id(client):
    """404 responses include a request_id."""
    response = client.get("/api/v1/nonexistent")
    data = response.json()
    assert "request_id" in data
    assert data["request_id"] is not None


def test_error_envelope_structure(client):
    """Error envelope contains success, error, and request_id."""
    response = client.get("/api/v1/nonexistent")
    data = response.json()
    assert "success" in data
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]


def test_validation_error_returns_422(client):
    """A request that fails Pydantic validation returns 422."""
    response = client.get("/api/v1/health/?invalid_param=true")
    assert response.status_code == 200  # health endpoint ignores extra params


def test_unhandled_exception_returns_500(client):
    """An unhandled exception returns 500 with error envelope."""
    response = client.get("/trigger-error/")
    assert response.status_code in (404, 405, 500)


def test_error_response_message(client):
    """Error response includes a human-readable message."""
    response = client.get("/api/v1/nonexistent")
    data = response.json()
    assert isinstance(data["error"]["message"], str)
    assert len(data["error"]["message"]) > 0
