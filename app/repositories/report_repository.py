import json

from sqlalchemy.orm import Session

from app.db.models import Report
from app.schemas.report import ReportData


class ReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, company_name: str, report_data: ReportData) -> Report:
        report = Report(
            company_name=company_name,
            report_data=report_data.model_dump_json(),
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_all(self) -> list[Report]:
        return (
            self.db.query(Report)
            .order_by(Report.created_at.desc())
            .all()
        )

    def get_by_id(self, report_id: int) -> Report | None:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def delete(self, report: Report) -> None:
        self.db.delete(report)
        self.db.commit()

    def parse_report_data(self, report: Report) -> ReportData:
        return ReportData.model_validate(json.loads(report.report_data))
