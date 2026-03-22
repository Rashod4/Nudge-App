from enum import Enum

from pydantic import BaseModel, Field

from backend.data.categories import Category


class InsightType(str, Enum):
    OVERSPENDING = "overspending"
    RECURRING_ALERT = "recurring_alert"
    POSITIVE_TREND = "positive_trend"
    WARNING = "warning"


class SuggestionType(str, Enum):
    REVIEW = "review"
    REDUCE = "reduce"
    CELEBRATE = "celebrate"
    MONITOR = "monitor"


class Insight(BaseModel):
    type: InsightType
    category: Category
    confidence: float = Field(ge=0.0, le=1.0)
    title: str = Field(max_length=100)
    message: str = Field(max_length=300)
    suggestion_type: SuggestionType
    source: str = "rule"  # "rule" or "ai"


class InsightResponse(BaseModel):
    """Schema for validating AI-generated insight responses."""
    insights: list[Insight]


class TransactionOut(BaseModel):
    id: int
    date: str
    raw_description: str
    amount: float
    type: str
    category: str


class CategoryBreakdown(BaseModel):
    category: str
    total: float
    count: int
    percentage: float


class SpendingSummary(BaseModel):
    total_spent: float
    total_income: float
    burn_rate_daily: float
    days_of_data: int
    category_breakdown: list[CategoryBreakdown]
