"""Operational probes with distinct orchestration semantics."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config.settings import settings
from app.database.session import check_db
from app.shared.responses.envelope import SuccessResponse, success

router = APIRouter(tags=["operations"])


class DependencyStatus(BaseModel):
    database: Literal["connected", "disconnected", "disabled"]


class HealthData(BaseModel):
    status: Literal["healthy", "ready", "not_ready", "alive"]
    environment: str
    version: str
    dependencies: DependencyStatus


async def _database_status() -> Literal["connected", "disconnected", "disabled"]:
    if not settings.DATABASE_URL:
        return "disabled"
    return "connected" if await check_db() else "disconnected"


def _payload(
    request: Request,
    status: Literal["healthy", "ready", "not_ready", "alive"],
    database: Literal["connected", "disconnected", "disabled"],
) -> dict[str, object]:
    return success(
        HealthData(
            status=status,
            environment=settings.ENVIRONMENT,
            version=settings.VERSION,
            dependencies=DependencyStatus(database=database),
        ).model_dump(),
        request_id=request.state.request_id,
    )


@router.get("/liveness", response_model=SuccessResponse[HealthData])
async def liveness(request: Request) -> dict[str, object]:
    """Process probe: does not call external dependencies."""
    return _payload(request, "alive", "disabled")


@router.get("/readiness", response_model=SuccessResponse[HealthData])
async def readiness(request: Request) -> JSONResponse:
    """Traffic probe: reports unavailable configured dependencies."""
    database = await _database_status()
    ready = database != "disconnected"
    return JSONResponse(
        status_code=200 if ready else 503,
        content=_payload(request, "ready" if ready else "not_ready", database),
    )


@router.get("/health", response_model=SuccessResponse[HealthData])
async def health(request: Request) -> dict[str, object]:
    """Diagnostic health summary for operators."""
    database = await _database_status()
    return _payload(request, "healthy", database)
