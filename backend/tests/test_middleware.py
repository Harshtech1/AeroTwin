"""Tests for middleware components: RequestID and CORS."""


def test_request_id_header_present(client):
    """Every response includes an X-Request-ID header."""
    response = client.get("/")
    assert "x-request-id" in response.headers


def test_request_id_generated_on_missing(client):
    """A UUID is generated when the client sends no request ID."""
    response = client.get("/")
    rid = response.headers["x-request-id"]
    assert rid is not None
    assert len(rid) > 0


def test_request_id_honours_client_value(client):
    """Client-supplied X-Request-ID is echoed back."""
    custom = "my-custom-trace-id"
    response = client.get("/", headers={"X-Request-ID": custom})
    assert response.headers["x-request-id"] == custom


def test_request_id_unique_per_request(client):
    """Each request gets a different request ID."""
    r1 = client.get("/")
    r2 = client.get("/")
    assert r1.headers["x-request-id"] != r2.headers["x-request-id"]


def test_cors_wildcard_origin(client):
    """CORS allows all origins by default."""
    response = client.options(
        "/",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers


def test_cors_allow_methods(client):
    """CORS exposes allowed methods."""
    response = client.options(
        "/",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    methods = response.headers.get("access-control-allow-methods", "")
    assert "GET" in methods or "POST" in methods


def test_request_id_on_error_response(client):
    """Error responses also carry X-Request-ID header."""
    response = client.get("/nonexistent-route-12345")
    assert response.status_code == 404
    assert "x-request-id" in response.headers
