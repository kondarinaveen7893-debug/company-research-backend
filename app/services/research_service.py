import asyncio
import json
from collections.abc import AsyncGenerator
from typing import Protocol

from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportData
from app.services.mock_research_provider import get_mock_research


class ResearchProvider(Protocol):
    def __call__(self, company_name: str) -> ReportData: ...


def _format_sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def stream_research(
    company_name: str,
    db: Session,
    provider: ResearchProvider = get_mock_research,
) -> AsyncGenerator[str, None]:
    try:
        report_data = provider(company_name)
    except Exception:
        yield _format_sse("error", {"message": "Research provider failed"})
        return

    sections = [
        ("overview", report_data.overview),
        ("key_people", [p.model_dump() for p in report_data.key_people]),
        ("news", report_data.news),
        ("financials", report_data.financials.model_dump()),
        ("risks", report_data.risks),
    ]

    for section_name, section_data in sections:
        yield _format_sse("section", {"section": section_name, "data": section_data})
        await asyncio.sleep(0.6)

    try:
        repo = ReportRepository(db)
        saved = repo.create(company_name, report_data)
        yield _format_sse("complete", {"report_id": saved.id})
    except Exception:
        yield _format_sse("error", {"message": "Failed to save report"})
