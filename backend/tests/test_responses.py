"""Response and pagination contract tests."""

import pytest
from app.shared.responses import PaginationParams, ResponseMeta, error, success
from pydantic import ValidationError


def test_success_envelope_with_metadata() -> None:
    result = success([1, 2], meta=ResponseMeta(page=2, page_size=2, total=5))
    assert result["success"] is True
    assert result["data"] == [1, 2]
    assert result["meta"]["total"] == 5


def test_error_envelope_omits_empty_details() -> None:
    result = error("CONFLICT", "Already exists", request_id="request-1")
    assert result == {
        "success": False,
        "error": {"code": "CONFLICT", "message": "Already exists"},
        "meta": {"request_id": "request-1"},
    }


def test_pagination_offset_and_limits() -> None:
    assert PaginationParams(page=3, page_size=10).offset == 20
    with pytest.raises(ValidationError):
        PaginationParams(page_size=101)
