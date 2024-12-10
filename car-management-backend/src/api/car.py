from fastapi import APIRouter, HTTPException, Query

from api.dependencies import UOWDep
from schemas.car import CarSchema, CarSchemaAdd, CarSchemaEdit
from services.car import CarService

router = APIRouter(
    prefix="/cars",
    tags=["Cars"],
)


@router.get("")
async def get_cars(
    uow: UOWDep,
    car_make: str = Query(None, alias="carMake"),
    garage_id: int = Query(None, alias="garageId"),
    from_year: str = Query(None, alias="fromYear"),
    to_year: str = Query(None, alias="toYear"),
) -> list[CarSchema]:
    filters = {
        "make": car_make,
        "garage_id": garage_id,
        "production_year__gte": from_year,
        "production_year__lte": to_year,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    tasks = await CarService().get_cars(uow, filters)
    return tasks


@router.post("")
async def add_car(
    car: CarSchemaAdd,
    uow: UOWDep,
) -> CarSchema:
    print(car)
    car = await CarService().add_car(uow, car)
    return car


@router.put("/{car_id}")
async def edit_car(
    car_id: int,
    car: CarSchemaEdit,
    uow: UOWDep,
) -> CarSchema:
    try:
        updated_car = await CarService().edit_car(uow, car_id, car)
        return updated_car
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{car_id}")
async def delete_car(
    car_id: int,
    uow: UOWDep,
):
    try:
        success = await CarService().delete_car(uow, car_id)
        return {"success": success}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
