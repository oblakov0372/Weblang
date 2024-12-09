from schemas.car import CarSchemaAdd
from utils.unitofwork import IUnitOfWork


class CarService:
    async def get_cars(self, uow: IUnitOfWork):
        async with uow:
            cars = await uow.cars.find_all()
            return cars

    async def add_car(self, uow: IUnitOfWork, car: CarSchemaAdd):
        car_dict = car.model_dump()
        print(car_dict)
        garage_ids = car_dict.pop("garage_ids", None)
        async with uow:
            car_id = await uow.cars.add_one(car_dict)
            await uow.commit()
            return car_id
