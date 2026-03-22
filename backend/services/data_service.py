# NOTE: This service layer abstracts data access. In a future iteration,
# these methods would become MCP tool definitions, allowing the AI agent
# to call them directly through the Model Context Protocol instead of
# receiving pre-built summaries. The interface stays the same.

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any

from backend.data.categories import Category, CATEGORY_KEYWORDS
from backend.data.transactions import TRANSACTIONS


class DataService:
    """Abstraction layer for all financial data access.
    Currently uses in-memory data.
    Future: swap to MCP tool calls without changing any other code.
    """

    def __init__(self) -> None:
        self._transactions: list[dict[str, Any]] = [self._enrich(t) for t in TRANSACTIONS]

    def _enrich(self, txn: dict[str, Any]) -> dict[str, Any]:
        """Add computed category to a transaction."""
        enriched = {**txn, "category": self._categorize(txn["raw_description"])}
        return enriched

    def _categorize(self, description: str) -> str:
        """Deterministic keyword-based categorization."""
        desc_lower = description.lower()
        for keyword, category in CATEGORY_KEYWORDS.items():
            if keyword in desc_lower:
                return category.value
        return Category.UNCATEGORIZED.value

    def _normalize_merchant(self, description: str) -> str:
        """Strip trailing codes/numbers for merchant grouping."""
        name = description.upper().strip()
        # Remove trailing hex codes, hash-numbers, asterisk prefixes
        name = re.sub(r"[#*]\S+$", "", name).strip()
        name = re.sub(r"\s+[A-F0-9]{4,}$", "", name).strip()
        name = re.sub(r"\s+\d{4,}$", "", name).strip()
        return name

    def _filter_by_timeframe(self, days: int | None = None) -> list[dict[str, Any]]:
        """Filter transactions to the last N days."""
        if days is None:
            return list(self._transactions)
        cutoff = datetime.now().date() - timedelta(days=days)
        return [
            t for t in self._transactions
            if datetime.strptime(t["date"], "%Y-%m-%d").date() >= cutoff
        ]

    def get_transactions(self, category: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        """Returns transactions, optionally filtered by category."""
        txns = list(self._transactions)
        if category:
            txns = [t for t in txns if t["category"] == category]
        txns.sort(key=lambda t: t["date"], reverse=True)
        return txns[:limit]

    def get_spending_summary(self, timeframe: str = "all") -> dict[str, Any]:
        """Returns spending totals by category for the given timeframe."""
        days_map = {"7d": 7, "14d": 14, "21d": 21, "all": None}
        days = days_map.get(timeframe)
        txns = self._filter_by_timeframe(days)

        total_spent = sum(abs(t["amount"]) for t in txns if t["amount"] < 0)
        total_income = sum(t["amount"] for t in txns if t["amount"] > 0)

        dates = [datetime.strptime(t["date"], "%Y-%m-%d").date() for t in txns]
        days_of_data = max((max(dates) - min(dates)).days, 1) if dates else 1
        burn_rate_daily = total_spent / days_of_data if days_of_data > 0 else 0

        breakdown = self.get_category_breakdown(days)
        return {
            "total_spent": round(total_spent, 2),
            "total_income": round(total_income, 2),
            "burn_rate_daily": round(burn_rate_daily, 2),
            "days_of_data": days_of_data,
            "category_breakdown": breakdown,
        }

    def get_category_breakdown(self, days: int | None = None) -> list[dict[str, Any]]:
        """Returns count and total per category."""
        txns = self._filter_by_timeframe(days)
        debits = [t for t in txns if t["amount"] < 0]
        total_spent = sum(abs(t["amount"]) for t in debits) or 1

        cats: dict[str, dict[str, Any]] = {}
        for t in debits:
            cat = t["category"]
            if cat not in cats:
                cats[cat] = {"category": cat, "total": 0.0, "count": 0}
            cats[cat]["total"] += abs(t["amount"])
            cats[cat]["count"] += 1

        result: list[dict[str, Any]] = []
        for info in cats.values():
            info["total"] = round(info["total"], 2)
            info["percentage"] = round(info["total"] / total_spent * 100, 1)
            result.append(info)

        result.sort(key=lambda x: x["total"], reverse=True)
        return result

    def get_recurring_charges(self) -> list[dict[str, Any]]:
        """Detects recurring charges based on merchant + amount patterns."""
        debits = [t for t in self._transactions if t["amount"] < 0]
        merchant_groups: dict[str, list[dict[str, Any]]] = {}

        for t in debits:
            key = self._normalize_merchant(t["raw_description"])
            if key not in merchant_groups:
                merchant_groups[key] = []
            merchant_groups[key].append(t)

        recurring: list[dict[str, Any]] = []
        for merchant, txns in merchant_groups.items():
            if len(txns) >= 2:
                amounts = [abs(t["amount"]) for t in txns]
                avg_amount = sum(amounts) / len(amounts)
                # Check if amounts are similar (within 20%)
                similar = all(abs(a - avg_amount) / avg_amount < 0.20 for a in amounts)
                if similar:
                    recurring.append({
                        "merchant": merchant,
                        "occurrences": len(txns),
                        "avg_amount": round(avg_amount, 2),
                        "category": txns[0]["category"],
                        "dates": [t["date"] for t in txns],
                    })

        recurring.sort(key=lambda x: x["avg_amount"], reverse=True)
        return recurring

    def get_budget_status(self, category: str) -> dict[str, Any]:
        """Returns budget vs actual for a category (weekly comparison)."""
        now = datetime.now().date()
        current_week = self._filter_by_timeframe(7)
        prior_week_start = now - timedelta(days=14)
        prior_week_end = now - timedelta(days=7)

        prior_week = [
            t for t in self._transactions
            if prior_week_start <= datetime.strptime(t["date"], "%Y-%m-%d").date() < prior_week_end
        ]

        def cat_total(txns: list[dict[str, Any]], cat: str) -> float:
            return sum(abs(t["amount"]) for t in txns if t["category"] == cat and t["amount"] < 0)

        current = cat_total(current_week, category)
        prior = cat_total(prior_week, category)
        change_pct = ((current - prior) / prior * 100) if prior > 0 else 0

        return {
            "category": category,
            "current_week": round(current, 2),
            "prior_week": round(prior, 2),
            "change_percent": round(change_pct, 1),
        }
