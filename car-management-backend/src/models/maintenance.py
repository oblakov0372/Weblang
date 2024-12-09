from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String, nullable=False)
    scheduled_date = Column(Date, nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    garage_id = Column(Integer, ForeignKey("garages.id"), nullable=False)

    car = relationship("Car", back_populates="maintenances")
    garage = relationship("Garage", back_populates="maintenances")
