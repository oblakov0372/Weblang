from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base
from schemas.garage import GarageSchema


class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    city = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    cars = relationship("Car", secondary="car_garages", back_populates="garages")
    maintenances = relationship("Maintenance", back_populates="garage")

    def to_read_model(self) -> GarageSchema:
        return GarageSchema(
            id=self.id,
            name=self.name,
            location=self.location,
            city=self.city,
            capacity=self.capacity,
        )
