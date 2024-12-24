from datetime import date

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import UOWDep
from schemas.car import CarSchema, CarSchemaAdd
from schemas.garage import GarageSchema, GarageSchemaAdd, GarageSchemaEdit
from schemas.reports import GarageDailyAvailabilityReportSchema
from services.car import CarService
from services.garage import GarageService

router = APIRouter(
    prefix="/garages",
    tags=["Garages"],
)


@router.get("")
async def get_garages(
    uow: UOWDep,
    city: str = Query(None),
) -> list[GarageSchema]:
    filters = {"city": city}
    filters = {k: v for k, v in filters.items() if v is not None}
    garages = await GarageService().get_garages(uow, filters)
    return garages


@router.post("")
async def add_garage(
    garage: GarageSchemaAdd,
    uow: UOWDep,
) -> GarageSchema:
    garage = await GarageService().add_garage(uow, garage)
    return garage


@router.delete("/{id}")
async def delete_garage(
    uow: UOWDep,
    id: int,
):
    success = await GarageService().delete_garage(uow, id)
    if not success:
        raise HTTPException(status_code=404, detail="Garage not found")
    return True


@router.put("/{garage_id}")
async def update_garage(
    uow: UOWDep,
    garage_id: int,
    garage: GarageSchemaEdit,
) -> GarageSchema:
    garage = await GarageService().update_garage(uow, garage_id, garage)
    return garage


@router.get("/dailyAvailabilityReport")
async def get_garage_report(
    uow: UOWDep,
    garage_id: int = Query(..., alias="garageId"),
    start_date: str = Query(..., alias="startDate"),
    end_date: str = Query(..., alias="endDate"),
):
    print(f"garage_id={garage_id}, start_date={start_date}, end_date={end_date}")
    try:
        result = await GarageService().get_garage_report(
            uow, garage_id, start_date, end_date
        )
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise


@router.get("/{id}")
async def get_garage(
    uow: UOWDep,
    id: int,
) -> GarageSchema:
    garages = await GarageService().get_garage(uow, id)
    return garages
