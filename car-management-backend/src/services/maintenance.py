from datetime import datetime, timedelta

from fastapi import HTTPException

from schemas.maintenance import (
    MaintenanceSchema,
    MaintenanceSchemaAdd,
    MaintenanceSchemaEdit,
)
from schemas.reports import MonthlyRequestsReportSchema, YearMonthSchema
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

    async def monthly_requests_report(
        self, uow: IUnitOfWork, garage_id: int, start_month: str, end_month: str
    ) -> list[MonthlyRequestsReportSchema]:
        async with uow:
            report_data = await uow.maintenances.get_monthly_requests_report(
                garage_id, start_month, end_month
            )

            start_date = datetime.strptime(start_month, "%Y-%m")
            end_date = datetime.strptime(end_month, "%Y-%m")

            months = []
            current_date = start_date
            while current_date <= end_date:
                months.append(current_date.strftime("%Y-%m"))
                current_date += timedelta(days=32)
                current_date = current_date.replace(day=1)

            result_dict = {
                f"{item.year_month.year}-{item.year_month.month_value:02d}": item.requests
                for item in report_data
            }

            report = []
            for month in months:
                year, month_value = month.split("-")
                report.append(
                    MonthlyRequestsReportSchema(
                        year_month=YearMonthSchema(
                            year=int(year),
                            month=month_value.upper(),
                            leap_year=int(year) % 4 == 0,
                            month_value=int(month_value),
                        ),
                        requests=result_dict.get(month, 0),
                    )
                )

            return report
