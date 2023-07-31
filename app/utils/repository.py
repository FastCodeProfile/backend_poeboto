from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update

from app.db.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, where_clause):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, where_clause):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_one(self, where_clause):
        async with async_session_maker() as session:
            stmt = select(self.model).where(where_clause)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_all(self, where_clause=None, by=None):
        async with async_session_maker() as session:
            stmt = select(self.model).where(where_clause)
            if by:
                stmt.order_by(by)
            res = await session.execute(stmt)
            res = [row[0] for row in res.all()]
            return res

    async def update(self, values, where_clause):
        async with async_session_maker() as session:
            stmt = update(self.model).values(**values).where(where_clause)
            await session.execute(stmt)
            await session.commit()
