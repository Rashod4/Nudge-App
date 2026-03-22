"""Deterministic rule-based detection engine.

Runs BEFORE the AI. Produces high-confidence insights from pure computation.
"""

from backend.data.categories import Category
from backend.engine.patterns import compute_category_trend, detect_frequency_change
from backend.validation.schemas import Insight, InsightType, SuggestionType


def run_rules(data_service) -> list[Insight]:
    """Run all deterministic rules and return validated insights."""
    insights: list[Insight] = []
    txns = data_service.get_transactions(limit=200)

    # Rule 1: Category spending spike (>30% increase week-over-week)
    for cat in Category:
        if cat in (Category.INCOME, Category.TRANSFER, Category.UNCATEGORIZED):
            continue
        trend = compute_category_trend(txns, cat.value)
        if trend["prior_week_total"] > 0 and trend["change_percent"] > 30:
            insights.append(Insight(
                type=InsightType.OVERSPENDING,
                category=cat,
                confidence=0.90,
                title=f"{cat.value.title()} spending up {trend['change_percent']:.0f}%",
                message=(
                    f"You spent ${trend['current_week_total']:.2f} on {cat.value} this week, "
                    f"up from ${trend['prior_week_total']:.2f} last week."
                ),
                suggestion_type=SuggestionType.REDUCE,
                source="rule",
            ))

    # Rule 2: Frequency detection (transaction count doubled)
    for cat in [Category.FOOD, Category.SHOPPING, Category.ENTERTAINMENT, Category.TRANSPORTATION]:
        freq = detect_frequency_change(txns, cat.value)
        if freq["prior_count"] > 0 and freq["frequency_ratio"] >= 1.8:
            insights.append(Insight(
                type=InsightType.WARNING,
                category=cat,
                confidence=0.88,
                title=f"{cat.value.title()} orders surging",
                message=(
                    f"You had {freq['current_count']} {cat.value} transactions this week "
                    f"vs {freq['prior_count']} last week — that's {freq['frequency_ratio']:.1f}x more."
                ),
                suggestion_type=SuggestionType.REVIEW,
                source="rule",
            ))

    # Rule 3: Recurring charge audit
    recurring = data_service.get_recurring_charges()
    for charge in recurring:
        if charge["category"] == "subscription" and charge["avg_amount"] > 10:
            insights.append(Insight(
                type=InsightType.RECURRING_ALERT,
                category=Category.SUBSCRIPTION,
                confidence=0.85,
                title=f"Recurring charge: ${charge['avg_amount']:.2f}/mo",
                message=(
                    f"A {charge['category']} charge of ~${charge['avg_amount']:.2f} "
                    f"has appeared {charge['occurrences']} times. "
                    f"Review whether you're still using this service."
                ),
                suggestion_type=SuggestionType.REVIEW,
                source="rule",
            ))

    # Rule 4: Burn rate warning
    summary = data_service.get_spending_summary("all")
    monthly_projected = summary["burn_rate_daily"] * 30
    monthly_income = summary["total_income"] / max(summary["days_of_data"] / 30, 1)
    if monthly_projected > monthly_income * 0.95:
        days_until_zero = (
            summary["total_income"] / summary["burn_rate_daily"]
            if summary["burn_rate_daily"] > 0 else 999
        )
        insights.append(Insight(
            type=InsightType.WARNING,
            category=Category.UNCATEGORIZED,
            confidence=0.92,
            title="Spending pace exceeds income",
            message=(
                f"At ${summary['burn_rate_daily']:.2f}/day, you're projected to spend "
                f"${monthly_projected:.0f}/mo against ~${monthly_income:.0f}/mo income. "
                f"At this rate, funds last ~{days_until_zero:.0f} days per pay cycle."
            ),
            suggestion_type=SuggestionType.REDUCE,
            source="rule",
        ))

    # Rule 5: Uncategorized spending alert
    total = len(txns)
    uncategorized = len([t for t in txns if t["category"] == "uncategorized"])
    if total > 0 and (uncategorized / total) > 0.20:
        insights.append(Insight(
            type=InsightType.WARNING,
            category=Category.UNCATEGORIZED,
            confidence=0.80,
            title=f"{uncategorized} transactions need review",
            message=(
                f"{uncategorized} of {total} transactions couldn't be automatically "
                f"categorized. Review them to get more accurate spending insights."
            ),
            suggestion_type=SuggestionType.REVIEW,
            source="rule",
        ))

    # Rule 6: Positive reinforcement (category decreased)
    for cat in Category:
        if cat in (Category.INCOME, Category.TRANSFER, Category.UNCATEGORIZED):
            continue
        trend = compute_category_trend(txns, cat.value)
        if trend["prior_week_total"] > 20 and trend["change_percent"] < -25:
            insights.append(Insight(
                type=InsightType.POSITIVE_TREND,
                category=cat,
                confidence=0.87,
                title=f"{cat.value.title()} spending down {abs(trend['change_percent']):.0f}%",
                message=(
                    f"Nice! You spent ${trend['current_week_total']:.2f} on {cat.value} "
                    f"this week, down from ${trend['prior_week_total']:.2f} last week."
                ),
                suggestion_type=SuggestionType.CELEBRATE,
                source="rule",
            ))

    # Sort by confidence descending
    insights.sort(key=lambda i: i.confidence, reverse=True)
    return insights
