from pydantic import BaseModel


class MaintanceSchema(BaseModel):
    id: int
    carId: int
    carName: str
    serviceType: str
    scheduleDate: str
    garageId: int
    garageName: str

    class Config:
        from_attributes = True


class MaintanceSchemaAdd(BaseModel):
    garageId: int
    carId: int
    serviceType: str
    scheduleDate: str


class MaintanceSchemaEdit(BaseModel):
    carId: int | None
    garageId: int | None
    scheduleDate: str | None
    serviceType: str | None
