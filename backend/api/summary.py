from typing import Any

from fastapi import APIRouter, Query

from backend.services.data_service import DataService

router = APIRouter(prefix="/api")


@router.get("/summary")
async def get_summary(timeframe: str = Query("all")) -> dict[str, Any]:
    ds = DataService()
    return ds.get_spending_summary(timeframe=timeframe)
