from models.car import Car
from repositories.repository import SQLAlchemyRepository


class CarRepository(SQLAlchemyRepository):
    model = Car
