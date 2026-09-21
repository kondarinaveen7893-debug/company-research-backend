from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ResearchRequest(BaseModel):
    company_name: str

    @field_validator("company_name")
    @classmethod
    def company_name_must_be_meaningful(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped or len(stripped) < 2:
            raise ValueError("company_name must be at least 2 characters")
        return stripped


class KeyPerson(BaseModel):
    name: str
    title: str


class Financials(BaseModel):
    revenue: Optional[str] = None
    employee_count: Optional[str] = None
    market_cap: Optional[str] = None
    yoy_growth: Optional[str] = None


class ReportData(BaseModel):
    overview: str
    key_people: list[KeyPerson]
    news: list[str]
    financials: Financials
    risks: list[str]


class ReportSummary(BaseModel):
    id: int
    company_name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportDetail(BaseModel):
    id: int
    company_name: str
    created_at: datetime
    report_data: ReportData

    model_config = {"from_attributes": True}


class DeleteResponse(BaseModel):
    message: str
