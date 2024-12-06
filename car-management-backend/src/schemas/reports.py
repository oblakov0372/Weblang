from pydantic import BaseModel


class YearMonthScheme(BaseModel):
    year: int
    month: str
    monthValue: int
    leapYear: bool


class MonthlyRequestsReportScheme(BaseModel):
    yearMonth: YearMonthScheme
    requests: int


class GarageDailyAvailabilityReportScheme(BaseModel):
    date: str
    requests: int
    availableCapacity: int
