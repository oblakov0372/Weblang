from models.car import Car
from schemas.car import CarSchema, CarSchemaAdd, CarSchemaEdit
from utils.unitofwork import IUnitOfWork


class CarService:
    async def get_cars(self, uow: IUnitOfWork, filters: dict) -> list[CarSchema]:
        async with uow:
            cars = await uow.cars.find_all_with_garages(filters)
            return cars

    async def add_car(self, uow: IUnitOfWork, car: CarSchemaAdd) -> CarSchema:
        car_dict = car.model_dump()
        print(car_dict)
        garage_ids = car_dict.pop("garage_ids", None)
        garages = []
        async with uow:
            if garage_ids:
                for garage_id in garage_ids:
                    garage = await uow.garages.find_by_id(garage_id)
                    if not garage:
                        raise ValueError(f"Garage with ID {garage_id} does not exist")
                    garages.append(garage)
                car_id = await uow.cars.add_with_garages(car_dict, garage_ids)

            await uow.commit()
            car_dto = CarSchema(id=car_id, **car_dict, garages=garages)
            return car_dto

    async def edit_car(
        self, uow: IUnitOfWork, car_id: int, car: CarSchemaEdit
    ) -> CarSchema:
        car_dict = car.model_dump()
        garage_ids = car_dict.pop("garage_ids", None)
        garages = []

        async with uow:
            if garage_ids:
                for garage_id in garage_ids:
                    garage = await uow.garages.find_by_id(garage_id)
                    if not garage:
                        raise ValueError(f"Garage with ID {garage_id} does not exist")
                    garages.append(garage)

            success = await uow.cars.edit_with_garages(car_id, car_dict, garage_ids)
            if not success:
                raise ValueError(f"Car with ID {car_id} does not exist")

            await uow.commit()

            car_dto = CarSchema(id=car_id, **car_dict, garages=garages)
            return car_dto

    async def delete_car(self, uow: IUnitOfWork, car_id: int) -> bool:
        async with uow:
            success = await uow.cars.delete_with_garages(car_id)
            if not success:
                raise ValueError(f"Car with ID {car_id} does not exist")
            await uow.commit()
            return success
