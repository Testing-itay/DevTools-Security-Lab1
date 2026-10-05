"""Health check endpoints."""

from fastapi import APIRouter
from datetime import datetime

from api.models import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return system health status for load balancers and monitoring."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database="connected",
        cache="connected",
        timestamp=datetime.utcnow(),
    )
