"""
Tests for root and health endpoints.

Verifies:
  - Root endpoint returns correct project name and status.
  - Health endpoint returns 200 with a SuccessResponse envelope.
  - Health response data contains 'status: ok' and 'version'.
  - Health response includes request_id.
"""


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "AeroTwin"
    assert data["status"] == "running"
    assert "version" in data


def test_health_check_status(client):
    """Health endpoint returns HTTP 200."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200


def test_health_check_envelope(client):
    """Health response is wrapped in SuccessResponse envelope."""
    response = client.get("/api/v1/health/")
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_health_check_data_fields(client):
    """Health data contains status, version, and database."""
    response = client.get("/api/v1/health/")
    data = response.json()["data"]
    assert data["status"] == "ok"
    assert "version" in data
    assert "database" in data


def test_health_check_request_id_in_response_header(client):
    """X-Request-ID header is present on health response."""
    response = client.get("/api/v1/health/")
    assert "x-request-id" in response.headers


def test_health_check_request_id_in_envelope(client):
    """request_id field appears in the response envelope."""
    response = client.get("/api/v1/health/")
    data = response.json()
    assert "request_id" in data


def test_health_honours_client_request_id(client):
    """If client sends X-Request-ID, the same ID is echoed back."""
    custom_id = "test-request-id-12345"
    response = client.get("/api/v1/health/", headers={"X-Request-ID": custom_id})
    assert response.headers.get("x-request-id") == custom_id
    assert response.json().get("request_id") == custom_id
