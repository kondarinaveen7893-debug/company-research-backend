# Company Research Backend

FastAPI backend for the Company Research Tool. Streams structured company research reports section-by-section using Server-Sent Events and persists completed reports to SQLite.

## Architecture

```
Request → Route → Research Service → Mock Provider → SSE Stream → SQLite
                                                              ↓
                                                    Report Repository
```

Responsibilities are strictly separated:

- **Routes** — HTTP concerns, request validation, response handling
- **Research Service** — orchestrates streaming, calls the provider, persists after completion
- **Mock Research Provider** — all static mock data in one place
- **Report Repository** — all database operations
- **Schemas** — Pydantic request/response models
- **Config** — environment-driven settings via Pydantic Settings

## Technology Choices

| Concern | Choice | Reason |
|---|---|---|
| Framework | FastAPI | Assignment requirement; async-native, automatic OpenAPI |
| Database | SQLite + SQLAlchemy | Assignment requirement; zero infrastructure |
| Streaming | Server-Sent Events | Assignment requirement; simpler than WebSockets for one-way push |
| Config | Pydantic Settings | Type-safe env loading, `.env` support |
| Testing | pytest + httpx | Standard FastAPI testing stack |

## Folder Structure

```
app/
├── main.py                        # App factory, middleware, startup
├── core/config.py                 # Pydantic Settings
├── db/
│   ├── database.py                # Engine, session, init_db
│   └── models.py                  # SQLAlchemy Report model
├── schemas/report.py              # Pydantic request/response models
├── repositories/report_repository.py  # DB operations
├── services/
│   ├── research_service.py        # SSE streaming orchestration
│   └── mock_research_provider.py  # Static mock data
└── api/routes/
    ├── health.py
    ├── research.py
    └── reports.py
tests/
├── conftest.py                    # Test DB, fixtures
├── test_health.py
├── test_research.py
└── test_reports.py
```

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Environment Configuration

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `company-research-backend` | Application name |
| `APP_ENV` | `development` | Environment label |
| `DATABASE_URL` | `sqlite:///./research.db` | SQLAlchemy database URL |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |
| `MOCK_RESEARCH_ENABLED` | `true` | Use mock provider (always true currently) |

Never commit `.env`. It is in `.gitignore`.

## Running

```bash
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

The SQLite database is created automatically on startup.

## Running Tests

```bash
pytest
```

Tests use a separate `test_research.db` that is created and torn down automatically. Never depends on the development database.

## API Endpoints

### GET /api/health

```json
{"status": "ok"}
```

### POST /api/research

Request:
```json
{"company_name": "Microsoft"}
```

Streams SSE events (see SSE Event Format below). Saves the report to SQLite after all sections are delivered.

### GET /api/reports

Returns a list of saved reports, newest first. Does not include full report data.

```json
[
  {"id": 1, "company_name": "Microsoft", "created_at": "2024-01-01T00:00:00Z"}
]
```

### GET /api/reports/{id}

Returns the full report including all five sections. Returns `404` if not found.

### DELETE /api/reports/{id}

Deletes the report. Returns `404` if not found.

## SSE Event Format

Each event follows the standard SSE format:

```
event: section
data: {"section": "overview", "data": "..."}

event: section
data: {"section": "key_people", "data": [...]}

event: section
data: {"section": "news", "data": [...]}

event: section
data: {"section": "financials", "data": {...}}

event: section
data: {"section": "risks", "data": [...]}

event: complete
data: {"report_id": 42}
```

On failure:
```
event: error
data: {"message": "..."}
```

Sections are delivered with a ~0.6s delay between them so the frontend can progressively render each section as it arrives.

## Mock Provider

All mock data lives in `app/services/mock_research_provider.py`. It supports:

- Microsoft
- Google
- Amazon
- Apple
- Salesforce

Unknown companies receive a graceful generic response with `null` financials and empty lists.

## Replacing the Mock with a Real Provider

The research service accepts any callable matching the `ResearchProvider` protocol:

```python
class ResearchProvider(Protocol):
    def __call__(self, company_name: str) -> ReportData: ...
```

To integrate a real LLM or search API:

1. Create `app/services/llm_research_provider.py` implementing the same signature.
2. Pass it to `stream_research` in the route, or wire it via dependency injection.
3. No changes needed to routes, schemas, or the database layer.

The `MOCK_RESEARCH_ENABLED` environment variable is already in place to gate which provider is selected.

## Trade-offs

- Report data is stored as a JSON blob in a single SQLite column. This is appropriate for the assignment scope and avoids over-engineering a relational schema for nested data.
- The SSE delay is a fixed `asyncio.sleep`. A real provider would have natural latency from LLM/search API calls.
- No authentication. The assignment does not require it.

## What Would Be Improved With More Time

- Real LLM provider (OpenAI / Anthropic) with streaming token output mapped to sections
- Real web search integration (Tavily / SerpAPI) for live news and financials
- Pagination on `GET /api/reports`
- Background task queue for long-running research jobs
- Structured logging
- Rate limiting
