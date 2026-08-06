"""
API v1 router registry.

Each endpoint module declares its own router with prefix and tags.
This file simply aggregates them under the top-level api_router which
main.py mounts at settings.API_V1_STR (default: /api/v1).
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(health.router)
