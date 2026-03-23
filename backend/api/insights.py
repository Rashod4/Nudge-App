from typing import Any

from fastapi import APIRouter

from backend.engine.ai_analyzer import analyze_with_ai
from backend.engine.rules import run_rules
from backend.services.data_service import DataService
from backend.validation.schemas import Insight

router = APIRouter(prefix="/api")


def _deduplicate(combined: list[Insight]) -> list[Insight]:
    """If both rule and AI flagged the same category+type, keep highest confidence."""
    seen: dict[str, dict[str, Any]] = {}
    for insight in combined:
        key = f"{insight.category.value}:{insight.type.value}"
        existing = seen.get(key)
        if existing is None or insight.confidence > existing["confidence"]:
            seen[key] = {"insight": insight, "confidence": insight.confidence}
    deduped: list[Insight] = [v["insight"] for v in seen.values()]
    deduped.sort(key=lambda i: i.confidence, reverse=True)
    return deduped[:10]


@router.get("/insights")
async def get_insights() -> dict[str, Any]:
    """Fast endpoint — returns rule-based insights only (instant)."""
    ds = DataService()
    rule_insights = run_rules(ds)

    return {
        "insights": [i.model_dump() for i in rule_insights],
        "rule_count": len(rule_insights),
        "ai_available": False,
        "ai_count": 0,
    }


@router.get("/insights/ai")
async def get_ai_insights() -> dict[str, Any]:
    """Slow endpoint — returns AI insights (called separately by frontend)."""
    ds = DataService()
    rule_insights = run_rules(ds)
    ai_insights, ai_available = await analyze_with_ai(ds)

    combined = _deduplicate(rule_insights + ai_insights)

    return {
        "insights": [i.model_dump() for i in combined],
        "ai_available": ai_available,
        "rule_count": len(rule_insights),
        "ai_count": len(ai_insights),
    }
