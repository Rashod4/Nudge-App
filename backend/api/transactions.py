from typing import Any

from fastapi import APIRouter, Query

from backend.services.data_service import DataService

router = APIRouter(prefix="/api")


@router.get("/transactions")
async def get_transactions(
    category: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
) -> list[dict[str, Any]]:
    ds = DataService()
    return ds.get_transactions(category=category, limit=limit)
