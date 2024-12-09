from fastapi import APIRouter

from api.dependencies import UOWDep
from schemas.car import CarSchema, CarSchemaAdd
from services.car import CarService

router = APIRouter(
    prefix="/cars",
    tags=["Cars"],
)


@router.get("")
async def get_cars(
    uow: UOWDep,
) -> list[CarSchema]:
    tasks = await CarService().get_cars(uow)
    return tasks


@router.post("")
async def add_car(
    car: CarSchemaAdd,
    uow: UOWDep,
):
    car_id = await CarService().add_car(uow, car)
    return {"car_id": car_id}
