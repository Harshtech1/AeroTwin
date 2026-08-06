"""
Sprint 2 test suite — core infrastructure tests.

Tests are organised into three modules:
  - test_main.py          (root + health endpoints)
  - test_middleware.py    (request_id, CORS)
  - test_exception_handlers.py (error envelopes)

conftest.py provides the shared TestClient fixture.
"""
