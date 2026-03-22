"""Spending pattern computation helpers.

Used by both the rules engine and the AI analyzer to compute
weekly spending trends and build the privacy-safe AI summary.
"""

from datetime import datetime, timedelta

from backend.data.categories import Category


def compute_weekly_spending(transactions: list[dict], num_weeks: int = 3) -> list[dict]:
    """Returns weekly spending totals for the last N weeks."""
    now = datetime.now().date()
    weeks = []
    for w in range(num_weeks):
        week_end = now - timedelta(days=w * 7)
        week_start = week_end - timedelta(days=7)
        week_txns = [
            t for t in transactions
            if t["amount"] < 0
            and week_start <= datetime.strptime(t["date"], "%Y-%m-%d").date() < week_end
        ]
        total = sum(abs(t["amount"]) for t in week_txns)
        weeks.append({
            "week": num_weeks - w,
            "start": str(week_start),
            "end": str(week_end),
            "total": round(total, 2),
            "count": len(week_txns),
        })
    weeks.reverse()
    return weeks


def compute_category_trend(transactions: list[dict], category: str) -> dict:
    """Returns week-over-week change for a category."""
    now = datetime.now().date()

    def week_total(offset_start: int, offset_end: int) -> tuple[float, int]:
        start = now - timedelta(days=offset_start)
        end = now - timedelta(days=offset_end)
        txns = [
            t for t in transactions
            if t["amount"] < 0
            and t["category"] == category
            and start <= datetime.strptime(t["date"], "%Y-%m-%d").date() < end
        ]
        return round(sum(abs(t["amount"]) for t in txns), 2), len(txns)

    current_total, current_count = week_total(7, 0)
    prior_total, prior_count = week_total(14, 7)
    change_pct = ((current_total - prior_total) / prior_total * 100) if prior_total > 0 else 0

    return {
        "category": category,
        "current_week_total": current_total,
        "current_week_count": current_count,
        "prior_week_total": prior_total,
        "prior_week_count": prior_count,
        "change_percent": round(change_pct, 1),
    }


def detect_frequency_change(transactions: list[dict], category: str) -> dict:
    """Returns current vs prior week transaction frequency for a category."""
    trend = compute_category_trend(transactions, category)
    prior_count = trend["prior_week_count"]
    current_count = trend["current_week_count"]
    ratio = (current_count / prior_count) if prior_count > 0 else float("inf") if current_count > 0 else 1.0

    return {
        "category": category,
        "current_count": current_count,
        "prior_count": prior_count,
        "frequency_ratio": round(ratio, 2),
    }


def build_ai_summary(data_service) -> str:
    """Build the aggregated summary sent to the AI.

    This is the PRIVACY BOUNDARY: only category totals, trends, and
    patterns are included. No merchant names or raw descriptions.
    """
    summary = data_service.get_spending_summary("all")
    recurring = data_service.get_recurring_charges()
    txns = data_service.get_transactions()

    # Compute trends for spending categories
    spending_cats = [c for c in Category if c not in (Category.INCOME, Category.UNCATEGORIZED)]
    trends = []
    for cat in spending_cats:
        trend = compute_category_trend(txns, cat.value)
        if trend["current_week_total"] > 0 or trend["prior_week_total"] > 0:
            trends.append(trend)

    # Frequency changes
    freq_changes = []
    for cat in spending_cats:
        freq = detect_frequency_change(txns, cat.value)
        if freq["current_count"] > 0 or freq["prior_count"] > 0:
            freq_changes.append(freq)

    # Build text summary
    lines = [
        "SPENDING SUMMARY:",
        f"  Total spent: ${summary['total_spent']:.2f}",
        f"  Total income: ${summary['total_income']:.2f}",
        f"  Daily burn rate: ${summary['burn_rate_daily']:.2f}/day",
        f"  Days of data: {summary['days_of_data']}",
        "",
        "CATEGORY BREAKDOWN:",
    ]
    for cat in summary["category_breakdown"]:
        lines.append(f"  {cat['category']}: ${cat['total']:.2f} ({cat['count']} transactions, {cat['percentage']}%)")

    lines.append("")
    lines.append("WEEK-OVER-WEEK TRENDS:")
    for t in trends:
        direction = "UP" if t["change_percent"] > 0 else "DOWN" if t["change_percent"] < 0 else "FLAT"
        lines.append(
            f"  {t['category']}: ${t['prior_week_total']:.2f} -> ${t['current_week_total']:.2f} "
            f"({direction} {abs(t['change_percent']):.0f}%), "
            f"frequency: {t['prior_week_count']} -> {t['current_week_count']} orders"
        )

    lines.append("")
    lines.append("FREQUENCY CHANGES:")
    for f in freq_changes:
        if f["frequency_ratio"] > 1.3 or f["frequency_ratio"] < 0.7:
            lines.append(
                f"  {f['category']}: {f['prior_count']} -> {f['current_count']} transactions "
                f"(ratio: {f['frequency_ratio']}x)"
            )

    lines.append("")
    lines.append("RECURRING CHARGES:")
    for r in recurring:
        lines.append(
            f"  {r['category']} subscription: ${r['avg_amount']:.2f}/occurrence, "
            f"{r['occurrences']} occurrences"
        )

    return "\n".join(lines)
