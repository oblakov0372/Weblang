from typing import List

from pydantic import BaseModel, Field

from schemas.garage import GarageSchema


class CarSchema(BaseModel):
    id: int | None
    make: str | None
    model: str | None
    production_year: int | None = Field(alias="productionYear")
    license_plate: str | None = Field(alias="licensePlate")
    garages: List["GarageSchema"] | None

    class Config:
        from_attributes = True
        populate_by_name = True


class CarSchemaAdd(BaseModel):
    make: str | None
    model: str | None
    production_year: int | None = Field(alias="productionYear")
    license_plate: str | None = Field(alias="licensePlate")
    garage_ids: List[int] | None = Field(alias="garageIds")

    class Config:
        populate_by_name = True


class CarSchemaEdit(CarSchemaAdd):
    pass
