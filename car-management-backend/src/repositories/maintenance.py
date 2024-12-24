from datetime import date

from sqlalchemy import func, insert, select
from sqlalchemy.orm import selectinload

from models import Maintenance
from models.garage import Garage
from repositories.repository import SQLAlchemyRepository
from schemas.maintenance import MaintenanceSchema
from schemas.reports import MonthlyRequestsReportSchema, YearMonthSchema


class MaintenanceRepository(SQLAlchemyRepository):
    model = Maintenance

    async def find_all_with_details(self, filters) -> list[MaintenanceSchema]:
        stmt = select(self.model).options(
            selectinload(self.model.car), selectinload(self.model.garage)
        )
        if filters.get("garage_id"):
            stmt = stmt.where(self.model.garage_id == filters["garage_id"])
        if filters.get("car_id"):
            stmt = stmt.where(self.model.car_id == filters["car_id"])
        if filters.get("start_date"):
            stmt = stmt.where(self.model.scheduled_date >= filters["start_date"])
        if filters.get("end_date"):
            stmt = stmt.where(self.model.scheduled_date <= filters["end_date"])
        res = await self.session.execute(stmt)
        return [row[0].to_read_model() for row in res.all()]

    async def find_by_id(self, id: int) -> MaintenanceSchema:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.car), selectinload(self.model.garage))
            .where(self.model.id == id)
        )
        res = await self.session.execute(stmt)
        record = res.scalar_one_or_none()
        print(record.car.make)
        print(record.garage.name)
        return record.to_read_model() if record else None

    async def add_one(self, data: dict) -> MaintenanceSchema:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        maintenance_id = res.scalar_one()

        return maintenance_id

    async def has_available_capacity(self, garage_id: int) -> bool:
        stmt = select(func.count(self.model.id)).where(
            self.model.garage_id == garage_id
        )

        print(self.model.garage_id)
        print(garage_id)

        res = await self.session.execute(stmt)
        current_count = res.scalar() or 0
        garage_stmt = select(Garage.capacity).where(Garage.id == garage_id)
        garage_res = await self.session.execute(garage_stmt)
        capacity = garage_res.scalar()

        return current_count < capacity

    async def get_monthly_requests_report(
        self, garage_id: int, start_month: str, end_month: str
    ) -> list[MonthlyRequestsReportSchema]:
        stmt = (
            select(
                func.strftime("%Y-%m", self.model.scheduled_date).label("year_month"),
                func.count(self.model.id).label("requests"),
            )
            .where(
                self.model.garage_id == garage_id,
                func.strftime("%Y-%m", self.model.scheduled_date) >= start_month,
                func.strftime("%Y-%m", self.model.scheduled_date) <= end_month,
            )
            .group_by("year_month")
        )

        res = await self.session.execute(stmt)
        results = res.all()

        return [
            MonthlyRequestsReportSchema(
                yearMonth=YearMonthSchema(
                    year=int(result.year_month.split("-")[0]),
                    month=result.year_month.split("-")[1].upper(),
                    leapYear=int(result.year_month.split("-")[0]) % 4 == 0,
                    monthValue=int(result.year_month.split("-")[1]),
                ),
                requests=result.requests,
            )
            for result in results
        ]
