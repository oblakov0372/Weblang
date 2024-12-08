from models.car import Car
from models.garage import Garage
from repositories.repository import SQLAlchemyRepository


class GarageRepository(SQLAlchemyRepository):
    model = Garage
