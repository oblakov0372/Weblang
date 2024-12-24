from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base
from schemas.maintenance import MaintenanceSchema


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String, nullable=False)
    scheduled_date = Column(Date, nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    garage_id = Column(
        Integer, ForeignKey("garages.id", ondelete="CASCADE"), nullable=False
    )

    car = relationship("Car", back_populates="maintenances")
    garage = relationship("Garage", back_populates="maintenances")

    def to_read_model(self) -> MaintenanceSchema:
        return MaintenanceSchema(
            id=self.id,
            car_id=self.car_id,
            car_name=f"{self.car.make} {self.car.model}" if self.car else None,
            service_type=self.service_type,
            scheduled_date=self.scheduled_date,
            garage_id=self.garage_id,
            garage_name=self.garage.name if self.garage else None,
        )
