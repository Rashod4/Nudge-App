from typing import Any

from fastapi import APIRouter

from backend.engine.ai_analyzer import analyze_with_ai
from backend.engine.rules import run_rules
from backend.services.data_service import DataService
from backend.validation.schemas import Insight

router = APIRouter(prefix="/api")


@router.get("/insights")
async def get_insights() -> dict[str, Any]:
    ds = DataService()

    # Step 1: Deterministic rule-based insights (always runs)
    rule_insights = run_rules(ds)

    # Step 2: AI-generated insights (may fail gracefully)
    ai_insights, ai_available = await analyze_with_ai(ds)

    # Step 3: Combine and deduplicate
    combined: list[Insight] = rule_insights + ai_insights

    # Deduplicate: if both rule and AI flagged the same category+type, keep highest confidence
    seen: dict[str, dict[str, Any]] = {}
    for insight in combined:
        key = f"{insight.category.value}:{insight.type.value}"
        existing = seen.get(key)
        if existing is None or insight.confidence > existing["confidence"]:
            seen[key] = {"insight": insight, "confidence": insight.confidence}

    deduped: list[Insight] = [v["insight"] for v in seen.values()]
    deduped.sort(key=lambda i: i.confidence, reverse=True)

    return {
        "insights": [i.model_dump() for i in deduped[:10]],
        "ai_available": ai_available,
        "rule_count": len(rule_insights),
        "ai_count": len(ai_insights),
    }
