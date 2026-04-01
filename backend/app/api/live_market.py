"""Live-market endpoints for real-world data snapshots."""
from fastapi import APIRouter, Query

from backend.app.core.live_market import live_market_service

router = APIRouter(prefix="/api/live-market", tags=["live-market"])


@router.get("/snapshot")
async def get_live_market_snapshot(refresh: bool = Query(False, description="Force a provider refresh")):
    return await live_market_service.get_snapshot(force_refresh=refresh)
