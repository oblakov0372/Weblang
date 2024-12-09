from datetime import date

from pydantic import BaseModel, Field


class MaintenanceSchema(BaseModel):
    id: int
    car_id: int = Field(alias="carId")
    car_name: str = Field(alias="carName")
    service_type: str = Field(alias="serviceType")
    schedule_date: date = Field(alias="scheduleDate")
    garage_id: int = Field(alias="garageId")
    garage_name: str = Field(alias="garageName")

    class Config:
        from_attributes = True
        populate_by_name = True


class MaintenanceSchemaAdd(BaseModel):
    garage_id: int = Field(alias="garageId")
    car_id: int = Field(alias="carId")
    service_type: str = Field(alias="serviceType")
    schedule_date: date = Field(alias="scheduleDate")

    class Config:
        populate_by_name = True


class MaintenanceSchemaEdit(BaseModel):
    car_id: int | None = Field(alias="carId")
    garage_id: int = Field(alias="garageId")
    schedule_date: date | None = Field(alias="scheduleDate")
    service_type: str | None = Field(alias="serviceType")

    class Config:
        populate_by_name = True
