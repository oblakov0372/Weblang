from typing import Optional

from pydantic import BaseModel

from schemas.garage import GarageSchema


class CarSchema(BaseModel):
    id: int | None
    make: str | None
    model: str | None
    productionYear: str | None
    licensePlate: str | None
    garages: list[GarageSchema] | None

    class Config:
        from_attributes = True


class CarSchemaAdd(BaseModel):
    make: str | None
    model: str | None
    productionYear: str | None
    licensePlate: str | None
    garageIds: list[int] | None


class CarSchemaEdit(BaseModel):
    make: str | None
    model: str | None
    productionYear: str | None
    licensePlate: str | None
    garageIds: list[int] | None
