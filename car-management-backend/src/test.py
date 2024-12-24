import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from db.db import DATABASE_URL
from models.car import Car


async def test_add_car():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        # Добавляем машину
        car = Car(
            make="Toyota",
            model="Corolla",
            production_year=2020,
            license_plate="ABC-1223s2",
        )
        session.add(car)
        await session.commit()

        # Проверяем, добавлена ли запись
        result = await session.execute(select(Car))
        cars = result.scalars().all()
        print(cars)


asyncio.run(test_add_car())
