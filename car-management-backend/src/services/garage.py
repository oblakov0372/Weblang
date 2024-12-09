from schemas.car import CarSchemaAdd
from schemas.garage import GarageSchemaAdd, GarageSchemaEdit
from utils.unitofwork import IUnitOfWork


class GarageService:
    async def get_garages(self, uow: IUnitOfWork, filters: dict):
        async with uow:
            garages = await uow.garages.find_all(filters)
            return garages

    async def add_garage(self, uow: IUnitOfWork, garage: GarageSchemaAdd):
        garage_dict = garage.model_dump()
        async with uow:
            garage_id = await uow.garages.add_one(garage_dict)
            await uow.commit()
            return garage_id

    async def delete_garage(self, uow: IUnitOfWork, garage_id: int) -> bool:
        async with uow:
            result = await uow.garages.delete_one(garage_id)
            await uow.commit()
            return result

    async def update_garage(
        self, uow: IUnitOfWork, garage_id: int, garage: GarageSchemaEdit
    ) -> bool:
        garage_data = garage.model_dump()
        async with uow:
            result = await uow.garages.edit_one(garage_id, garage_data)
            await uow.commit()
            return result
