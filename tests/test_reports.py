import json

import pytest

from app.db.models import Report
from app.schemas.report import Financials, KeyPerson, ReportData


def _seed_report(db_session, company_name: str = "Google") -> Report:
    data = ReportData(
        overview="Test overview",
        key_people=[KeyPerson(name="Jane Doe", title="CEO")],
        news=["News item one"],
        financials=Financials(revenue="$100B", employee_count="50,000", market_cap="$500B", yoy_growth="10%"),
        risks=["Risk one"],
    )
    report = Report(company_name=company_name, report_data=data.model_dump_json())
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    return report


def test_list_reports_empty(client):
    response = client.get("/api/reports")
    assert response.status_code == 200
    assert response.json() == []


def test_list_reports_returns_summaries(client, db_session):
    _seed_report(db_session, "Google")
    response = client.get("/api/reports")
    assert response.status_code == 200
    reports = response.json()
    assert len(reports) == 1
    assert reports[0]["company_name"] == "Google"
    assert "id" in reports[0]
    assert "created_at" in reports[0]
    assert "report_data" not in reports[0]


def test_get_report_returns_full_data(client, db_session):
    report = _seed_report(db_session, "Amazon")
    response = client.get(f"/api/reports/{report.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["company_name"] == "Amazon"
    assert "report_data" in body
    assert body["report_data"]["overview"] == "Test overview"
    assert body["report_data"]["key_people"][0]["name"] == "Jane Doe"


def test_get_report_404_for_missing(client):
    response = client.get("/api/reports/99999")
    assert response.status_code == 404


def test_delete_report(client, db_session):
    report = _seed_report(db_session, "Salesforce")
    response = client.delete(f"/api/reports/{report.id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    get_response = client.get(f"/api/reports/{report.id}")
    assert get_response.status_code == 404


def test_delete_report_404_for_missing(client):
    response = client.delete("/api/reports/99999")
    assert response.status_code == 404


def test_list_reports_ordered_newest_first(client, db_session):
    _seed_report(db_session, "Microsoft")
    _seed_report(db_session, "Apple")
    response = client.get("/api/reports")
    assert response.status_code == 200
    reports = response.json()
    assert len(reports) == 2
    assert reports[0]["company_name"] == "Apple"
    assert reports[1]["company_name"] == "Microsoft"
