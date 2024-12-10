from abc import ABC, abstractmethod

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, filters: dict = None):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by):
        raise NotImplementedError

    abstractmethod

    async def find_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> bool:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = (
            update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, filters: dict = None):
        stmt = select(self.model)

        if filters:
            stmt = stmt.filter(
                and_(
                    *[
                        getattr(self.model, key).like(f"%{value}%")
                        for key, value in filters.items()
                    ]
                )
            )

        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        record = res.scalar_one_or_none()
        if not record:
            return None
        return record.to_read_model()

    async def find_by_id(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        record = res.scalar_one_or_none()
        if not record:
            return None
        return record.to_read_model()

    async def delete_one(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
