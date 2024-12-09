from datetime import date

from pydantic import BaseModel, Field


class YearMonthSchema(BaseModel):
    year: int
    month: str
    month_value: int = Field(alias="monthValue")
    leap_year: bool = Field(alias="leapYear")

    class Config:
        populate_by_name = True


class MonthlyRequestsReportSchema(BaseModel):
    year_month: YearMonthSchema = Field(alias="yearMonth")
    requests: int

    class Config:
        populate_by_name = True


class GarageDailyAvailabilityReportSchema(BaseModel):
    date: date
    requests: int
    available_capacity: int = Field(alias="availableCapacity")

    class Config:
        populate_by_name = True
