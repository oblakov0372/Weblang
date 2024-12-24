from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from models import Garage, Maintenance
from repositories.repository import SQLAlchemyRepository
from schemas.reports import GarageDailyAvailabilityReportSchema


class GarageRepository(SQLAlchemyRepository):
    model = Garage

    async def get_garage_report(
        self, garage_id: int, start_date: str, end_date: str
    ) -> list[GarageDailyAvailabilityReportSchema]:

        stmt = (
            select(
                func.date(Maintenance.scheduled_date).label("date"),
                func.count(Maintenance.id).label("requests"),
                (Garage.capacity - func.count(Maintenance.id)).label(
                    "available_capacity"
                ),
            )
            .join(Garage, Garage.id == Maintenance.garage_id)
            .where(
                Maintenance.garage_id == garage_id,
                Maintenance.scheduled_date >= start_date,
                Maintenance.scheduled_date <= end_date,
            )
            .group_by("date", Garage.capacity)
        )

        res = await self.session.execute(stmt)
        results = res.all()
        print("Database results:", results)

        return [
            GarageDailyAvailabilityReportSchema(
                date=result.date,
                requests=result.requests,
                available_capacity=result.available_capacity,
            )
            for result in results
        ]
