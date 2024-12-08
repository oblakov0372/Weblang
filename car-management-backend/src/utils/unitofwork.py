from abc import ABC, abstractmethod
from typing import Type

from db.db import async_session_maker
from repositories.car import CarRepository
from repositories.garage import GarageRepository
from repositories.maintenance import MaintenanceRepository


class IUnitOfWork(ABC):
    cars: Type[CarRepository]
    garages: Type[GarageRepository]
    maintances: Type[MaintenanceRepository]

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.cars = CarRepository(self.session)
        self.garages = GarageRepository(self.session)
        self.maintenances = MaintenanceRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
