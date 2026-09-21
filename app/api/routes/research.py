from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.report import ResearchRequest
from app.services.research_service import stream_research

router = APIRouter()


@router.post("/research")
async def research(
    request: ResearchRequest,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    return StreamingResponse(
        stream_research(request.company_name, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
