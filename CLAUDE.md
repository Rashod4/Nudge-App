# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Project

**Backend** (FastAPI, port 8000):
```bash
PYTHONPATH=. python -m uvicorn backend.main:app --reload --port 8000
```
Requires `pip install -r backend/requirements.txt` and optionally `GEMINI_API_KEY` in `.env` (loaded via python-dotenv in `backend/main.py`).

**Frontend** (React + Vite, port 5173):
```bash
cd frontend && npm run dev
```
Vite proxies `/api/*` to `localhost:8000` (configured in `frontend/vite.config.js`).

**Lint:** `cd frontend && npx eslint src/` (ESLint 9 flat config)

No test framework is currently set up.

## Architecture

Nudge is a financial coaching tool where **AI is treated as an untrusted component**. The pipeline:

1. **DataService** (`backend/services/data_service.py`) — sole data access layer over in-memory transactions. All routes and engines import this; nothing imports `TRANSACTIONS` directly. Designed as a future MCP tool interface.

2. **Rule Engine** (`backend/engine/rules.py`) — runs first, always. Six deterministic rules (spending spikes, frequency changes, recurring charges, burn rate, uncategorized alerts, positive trends). Returns `list[Insight]` with `source="rule"`.

3. **AI Analyzer** (`backend/engine/ai_analyzer.py`) — sends only aggregated summaries (never raw merchant names) to Gemini via `build_ai_summary()` in `patterns.py`. Response is validated through Pydantic (`InsightResponse`), then post-filtered by business rules (remove rent/utility cut suggestions, cap confidence, limit to 5).

4. **Graceful degradation** — if AI fails (no API key, API error, invalid JSON, schema validation failure), the `/api/insights` endpoint returns rule-based insights only with `ai_available: false`.

5. **Deduplication** — when both rule and AI flag the same category+type, the higher-confidence insight wins.

## Key Patterns

- **`PYTHONPATH=.`** is required — all Python imports use `backend.*` paths from the repo root.
- **`from __future__ import annotations`** is used in engine files for forward-referencing `DataService` via `TYPE_CHECKING`. Must appear before any non-docstring code.
- **Category enum** (`backend/data/categories.py`) is the strict whitelist. AI responses with unknown categories are rejected by Pydantic.
- **`CATEGORY_KEYWORDS`** dict in `categories.py` drives deterministic merchant-to-category mapping via substring matching on lowercased descriptions.
- **Frontend fetches all 4 endpoints in parallel** via `Promise.all()` in `Dashboard.jsx`.

## Git Workflow

After completing a meaningful unit of work (new feature, bug fix, refactor, or set of related changes), commit and push to avoid losing progress. Don't batch up many unrelated changes — commit early and often. Use descriptive commit messages that explain *why*, not just *what*.

## API Endpoints

| Endpoint | AI? | Description |
|---|---|---|
| `GET /api/insights` | Yes | Full pipeline: rules + AI + validation + dedup |
| `GET /api/summary?timeframe=` | No | Spending breakdown and burn rate |
| `GET /api/transactions?category=&limit=` | No | Transaction list |
| `GET /api/categories` | No | Category whitelist |
