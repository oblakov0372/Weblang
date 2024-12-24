from fastapi import HTTPException

from schemas.maintenance import (
    MaintenanceSchema,
    MaintenanceSchemaAdd,
    MaintenanceSchemaEdit,
)
from utils.unitofwork import IUnitOfWork


class MaintenanceService:
    async def get_maintenances(
        self, uow: IUnitOfWork, filters: dict
    ) -> list[MaintenanceSchema]:
        async with uow:
            maintenances = await uow.maintenances.find_all_with_details(filters)
            return maintenances

    async def add_maintenance(
        self, uow: IUnitOfWork, maintenance: MaintenanceSchemaAdd
    ) -> MaintenanceSchema:
        maintenance_data = maintenance.model_dump()

        async with uow:
            has_capacity = await uow.maintenances.has_available_capacity(
                maintenance_data["garage_id"]
            )
            if not has_capacity:
                raise HTTPException(
                    status_code=400,
                    detail="No available capacity in the garage.",
                )

            maintenance_id = await uow.maintenances.add_one(maintenance_data)

            full_maintenance = await uow.maintenances.find_by_id(maintenance_id)
            await uow.commit()

            return full_maintenance

    async def update_maintenance(
        self, uow: IUnitOfWork, maintenance_id: int, maintenance: MaintenanceSchemaEdit
    ) -> MaintenanceSchema:
        maintenance_data = maintenance.model_dump()
        async with uow:
            updated_id = await uow.maintenances.edit_one(
                maintenance_id, maintenance_data
            )
            await uow.commit()
            return MaintenanceSchema(id=updated_id, **maintenance_data)

    async def delete_maintenance(self, uow: IUnitOfWork, maintenance_id: int) -> bool:
        async with uow:
            success = await uow.maintenances.delete_one(maintenance_id)
            await uow.commit()
            return success
