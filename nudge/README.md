# Nudge — Financial Intelligence Engine

Nudge is an autonomous financial coaching tool that analyzes transaction data to deliver proactive spending insights. Its core architectural principle: **AI is treated as an untrusted component** with deterministic validation layers around it.

## Architecture

```
Transactions → Rule Engine → Structured Summary → Claude API → Pydantic Validation → Business Rules → Dashboard
                  ↓                                                                                      ↑
            Rule-based insights ──────────────────────────────────────────────────────────────────────────┘
```

1. **Deterministic rule engine** runs first — computes spending trends, detects recurring charges, flags anomalies
2. **Privacy boundary** — only aggregated summaries (never raw merchant names or transaction details) are sent to the AI
3. **Pydantic v2 validation** — AI responses must conform to strict schemas (valid categories, confidence ranges, allowed types)
4. **Business rule post-validation** — removes unsafe suggestions (e.g., "cut rent"), caps insight count, adjusts low-confidence items
5. **Graceful degradation** — if the AI fails for any reason, the dashboard falls back to rule-based insights only

## Tech Stack

- **Frontend:** React (Vite) + Tailwind CSS + Recharts
- **Backend:** Python FastAPI
- **AI:** Anthropic Claude API (claude-sonnet-4-20250514)
- **Validation:** Pydantic v2
- **Database:** In-memory (mock transaction dataset)

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key (optional — works without it using rule engine only)

### Backend

```bash
cd nudge/backend
pip install -r requirements.txt

# Optional: set API key for AI-powered insights
export ANTHROPIC_API_KEY=your-key-here

# Start the server
cd ..
PYTHONPATH=. python -m uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd nudge/frontend
npm install
npm run dev
```

Visit `http://localhost:5173` — the Vite dev server proxies `/api` requests to the backend.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/transactions?category=&limit=` | Transaction list with optional filtering |
| `GET /api/categories` | Category whitelist |
| `GET /api/summary?timeframe=` | Spending breakdown and burn rate (no AI) |
| `GET /api/insights` | Full pipeline: rules + AI + validation |

## Future: MCP Integration

The `DataService` class in `backend/services/data_service.py` is an abstraction layer that currently reads from in-memory data. In a future iteration, these methods would become **MCP (Model Context Protocol) tool definitions**, allowing the AI agent to call them directly instead of receiving pre-built summaries.

The interface stays the same — only the data source changes:

```python
# Today: reads from Python list
ds.get_spending_summary("7d")

# Future: becomes an MCP tool the AI can invoke
@mcp.tool()
def get_spending_summary(timeframe: str) -> dict:
    ...
```

This enables the AI to autonomously decide what data it needs, while the MCP tool layer enforces access controls and data minimization.

## Privacy Considerations

- **Data minimization:** The AI receives only aggregated category totals and trends — never raw merchant names, account numbers, or transaction descriptions
- **Consent boundary:** In production, AI processing would require explicit user consent
- **Validation as guardrail:** Even if the AI hallucinates categories or amounts, Pydantic rejects invalid responses before they reach the user
- **Local option:** The architecture supports swapping to a local model for on-premises inference
