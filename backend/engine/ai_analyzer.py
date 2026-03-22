# PRIVACY NOTE: This module sends ONLY aggregated, anonymized spending summaries
# to the AI API. Raw transaction descriptions, merchant names, account details,
# and personally identifiable information are NEVER transmitted.
# In production, this would include:
# - Data minimization (send only what AI needs)
# - Consent flows before any AI processing
# - Data processing agreements with AI provider
# - Option for local model inference to keep data on-premises

import json
import logging
import os

import anthropic

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.services.data_service import DataService

from backend.data.categories import Category
from backend.engine.patterns import build_ai_summary
from backend.validation.schemas import (
    Insight,
    InsightResponse,
    InsightType,
    SuggestionType,
)

logger = logging.getLogger(__name__)

ALLOWED_CATEGORIES = ", ".join(c.value for c in Category)

SYSTEM_PROMPT = """You are a financial analysis engine. You generate actionable, \
empathetic insights for a user based on their aggregated spending data.

RULES:
- Only reference categories from this list: {categories}
- Never suggest reducing essential expenses (rent, utilities)
- If you are not confident about an insight, set confidence below 0.5
- Return ONLY valid JSON matching the required schema — no markdown, no explanation
- Do not invent data that isn't in the summary
- Maximum 5 insights
- Be specific with dollar amounts from the data provided""".format(categories=ALLOWED_CATEGORIES)

USER_PROMPT_TEMPLATE = """Based on the following spending data, generate actionable insights.

{summary}

Return a JSON object with this exact structure:
{{
  "insights": [
    {{
      "type": "overspending | recurring_alert | positive_trend | warning",
      "category": "<from allowed category list>",
      "confidence": <0.0 to 1.0>,
      "title": "<short headline, max 100 chars>",
      "message": "<1-2 sentence explanation, max 300 chars>",
      "suggestion_type": "review | reduce | celebrate | monitor"
    }}
  ]
}}"""


async def analyze_with_ai(data_service: "DataService") -> tuple[list[Insight], bool]:
    """Call Claude API with spending summary and validate the response.

    Returns:
        Tuple of (list of validated insights, bool indicating AI was available)
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY not set — skipping AI analysis")
        return [], False

    try:
        summary_text = build_ai_summary(data_service)

        client = anthropic.AsyncAnthropic(api_key=api_key)
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(summary=summary_text)}
            ],
        )

        raw_text = response.content[0].text

        # Parse JSON — handle cases where AI wraps in markdown code blocks
        json_text = raw_text.strip()
        if json_text.startswith("```"):
            json_text = json_text.split("\n", 1)[1]  # Remove opening ```json
            json_text = json_text.rsplit("```", 1)[0]  # Remove closing ```

        parsed = json.loads(json_text)

        # Validate with Pydantic
        validated = InsightResponse.model_validate(parsed)

        # Post-validation business rules
        insights = _apply_business_rules(validated.insights)

        return insights, True

    except anthropic.APIError as e:
        logger.error("Claude API error: %s", e)
        return [], False
    except json.JSONDecodeError as e:
        logger.error("AI returned invalid JSON: %s", e)
        return [], False
    except Exception as e:
        logger.error("AI analysis failed: %s", e)
        return [], False


def _apply_business_rules(insights: list[Insight]) -> list[Insight]:
    """Apply business rules on top of Pydantic-validated AI insights."""
    filtered: list[Insight] = []
    for insight in insights:
        # Remove suggestions to cut essential expenses
        if insight.category in (Category.RENT, Category.UTILITIES):
            if insight.suggestion_type in (SuggestionType.REDUCE,):
                continue

        # Low confidence → force to "review"
        if insight.confidence < 0.5:
            insight = insight.model_copy(update={"suggestion_type": SuggestionType.REVIEW})

        # Mark source as AI
        insight = insight.model_copy(update={"source": "ai"})

        filtered.append(insight)

    # Cap at 5 insights, sorted by confidence
    filtered.sort(key=lambda i: i.confidence, reverse=True)
    return filtered[:5]
