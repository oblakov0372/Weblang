from datetime import date

from pydantic import BaseModel


class MaintenanceSchema(BaseModel):
    id: int
    carId: int
    carName: str
    serviceType: str
    scheduleDate: date
    garageId: int
    garageName: str

    class Config:
        from_attributes = True


class MaintenanceSchemaAdd(BaseModel):
    garageId: int
    carId: int
    serviceType: str
    scheduleDate: date


class MaintenanceSchemaEdit(BaseModel):
    carId: int | None
    garageId: int  # Обязательное поле
    scheduleDate: date | None
    serviceType: str | None
