from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.orm import selectinload

from models.car import Car, car_garages
from models.garage import Garage
from repositories.repository import SQLAlchemyRepository


class CarRepository(SQLAlchemyRepository):
    model = Car

    async def find_all_with_garages(self, filters: dict = None):
        stmt = select(self.model).options(selectinload(self.model.garages))

        if filters:
            conditions = []
            for key, value in filters.items():
                if "__gte" in key:
                    column = key.replace("__gte", "")
                    conditions.append(getattr(self.model, column) >= value)
                elif "__lte" in key:
                    column = key.replace("__lte", "")
                    conditions.append(getattr(self.model, column) <= value)
                elif "garage_id" in key:
                    stmt = stmt.join(self.model.garages).filter(Garage.id == value)
                else:
                    conditions.append(getattr(self.model, key).like(f"%{value}%"))

            if conditions:
                stmt = stmt.filter(and_(*conditions))

        res = await self.session.execute(stmt)
        return [row[0].to_read_model() for row in res.all()]

    async def add_with_garages(
        self, car_data: dict, garage_ids: list[int] = None
    ) -> int:
        stmt = insert(self.model).values(**car_data).returning(self.model.id)
        res = await self.session.execute(stmt)
        car_id = res.scalar_one()

        if garage_ids:
            car_garage_links = [
                {"car_id": car_id, "garage_id": garage_id} for garage_id in garage_ids
            ]
            stmt = insert(car_garages).values(car_garage_links)
            await self.session.execute(stmt)

        return car_id

    async def edit_with_garages(
        self, car_id: int, car_data: dict, garage_ids: list[int] = None
    ) -> bool:
        stmt = update(self.model).where(self.model.id == car_id).values(**car_data)
        res = await self.session.execute(stmt)

        if garage_ids is not None:
            delete_stmt = delete(car_garages).where(car_garages.c.car_id == car_id)
            await self.session.execute(delete_stmt)

            if garage_ids:
                car_garage_links = [
                    {"car_id": car_id, "garage_id": garage_id}
                    for garage_id in garage_ids
                ]
                insert_stmt = insert(car_garages).values(car_garage_links)
                await self.session.execute(insert_stmt)

        return res.rowcount > 0

    async def delete_with_garages(self, car_id: int) -> bool:
        delete_stmt = delete(car_garages).where(car_garages.c.car_id == car_id)
        await self.session.execute(delete_stmt)

        delete_car_stmt = delete(self.model).where(self.model.id == car_id)
        result = await self.session.execute(delete_car_stmt)
        return result.rowcount > 0
