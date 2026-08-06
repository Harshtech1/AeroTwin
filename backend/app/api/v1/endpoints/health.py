from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request
from sqlalchemy import text

from app.constants.application import VERSION
from app.database.session import _AsyncSessionLocal
from app.shared.responses.envelope import SuccessResponse, success

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=SuccessResponse[dict[str, Any]])
async def get_health(request: Request) -> dict:
    request_id: str | None = getattr(request.state, "request_id", None)

    db_status = "unknown"
    if _AsyncSessionLocal is not None:
        try:
            async with _AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception:
            db_status = "disconnected"

    return success(
        data={
            "status": "ok",
            "version": VERSION,
            "database": db_status,
        },
        request_id=request_id,
    )
