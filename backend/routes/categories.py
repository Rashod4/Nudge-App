from fastapi import APIRouter

from backend.data.categories import Category

router = APIRouter(prefix="/api")


@router.get("/categories")
async def get_categories() -> list[dict[str, str]]:
    return [{"name": c.value, "label": c.value.title()} for c in Category]
