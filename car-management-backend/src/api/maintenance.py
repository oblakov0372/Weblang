from datetime import date

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import UOWDep
from schemas.maintenance import (
    MaintenanceSchema,
    MaintenanceSchemaAdd,
    MaintenanceSchemaEdit,
)
from schemas.reports import MonthlyRequestsReportSchema
from services.maintenance import MaintenanceService

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


@router.get("")
async def get_maintenances(
    uow: UOWDep,
    car_id: str = Query(None, alias="carId"),
    garage_id: int = Query(None, alias="garageId"),
    start_date: str = Query(None, alias="startDate"),
    end_date: str = Query(None, alias="endDate"),
) -> list[MaintenanceSchema]:
    filters = {
        "car_id": car_id,
        "garage_id": garage_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    maintenances = await MaintenanceService().get_maintenances(uow, filters)
    return maintenances


@router.post("")
async def add_maintenance(
    maintenance: MaintenanceSchemaAdd,
    uow: UOWDep,
) -> MaintenanceSchema:
    return await MaintenanceService().add_maintenance(uow, maintenance)


@router.put("/{id}")
async def update_maintenance(
    id: int,
    maintenance: MaintenanceSchemaEdit,
    uow: UOWDep,
) -> MaintenanceSchema:
    return await MaintenanceService().update_maintenance(uow, id, maintenance)


@router.delete("/{id}")
async def delete_maintenance(id: int, uow: UOWDep):
    success = await MaintenanceService().delete_maintenance(uow, id)
    if not success:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return {"success": True}


@router.get("/monthlyRequestsReport", response_model=list[MonthlyRequestsReportSchema])
async def monthly_requests_report(
    uow: UOWDep,
    garage_id: int = Query(..., alias="garageId"),
    start_month: str = Query(..., alias="startMonth"),
    end_month: str = Query(..., alias="endMonth"),
) -> list[MonthlyRequestsReportSchema]:
    return await MaintenanceService().monthly_requests_report(
        uow, garage_id, start_month, end_month
    )
