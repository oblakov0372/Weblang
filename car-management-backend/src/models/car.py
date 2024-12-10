from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db.db import Base
from schemas.car import CarSchema
from schemas.garage import GarageSchema

car_garages = Table(
    "car_garages",
    Base.metadata,
    Column("car_id", Integer, ForeignKey("cars.id"), primary_key=True),
    Column("garage_id", Integer, ForeignKey("garages.id"), primary_key=True),
)


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    production_year = Column(Integer, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)

    garages = relationship("Garage", secondary=car_garages, back_populates="cars")
    maintenances = relationship("Maintenance", back_populates="car")

    def to_read_model(self) -> CarSchema:
        return CarSchema(
            id=self.id,
            make=self.make,
            model=self.model,
            production_year=self.production_year,
            license_plate=self.license_plate,
            garages=[garage.to_read_model() for garage in self.garages],
        )
