from pydantic import BaseModel, Field


class GarageSchema(BaseModel):
    id: int
    name: str
    location: str
    city: str
    capacity: int

    class Config:
        from_attributes = True


class GarageSchemaAdd(BaseModel):
    name: str
    location: str
    city: str = Field(alias="City")
    capacity: int


class GarageSchemaEdit(BaseModel):
    name: str | None
    location: str | None
    capacity: int | None
    city: str | None
