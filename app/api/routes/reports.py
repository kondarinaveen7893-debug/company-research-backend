from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.report_repository import ReportRepository
from app.schemas.report import DeleteResponse, ReportDetail, ReportSummary

router = APIRouter()


@router.get("/reports", response_model=list[ReportSummary])
async def list_reports(db: Session = Depends(get_db)) -> list[ReportSummary]:
    repo = ReportRepository(db)
    reports = repo.list_all()
    return [ReportSummary.model_validate(r) for r in reports]


@router.get("/reports/{report_id}", response_model=ReportDetail)
async def get_report(report_id: int, db: Session = Depends(get_db)) -> ReportDetail:
    repo = ReportRepository(db)
    report = repo.get_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportDetail(
        id=report.id,
        company_name=report.company_name,
        created_at=report.created_at,
        report_data=repo.parse_report_data(report),
    )


@router.delete("/reports/{report_id}", response_model=DeleteResponse)
async def delete_report(report_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    repo = ReportRepository(db)
    report = repo.get_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    repo.delete(report)
    return DeleteResponse(message=f"Report {report_id} deleted successfully")
