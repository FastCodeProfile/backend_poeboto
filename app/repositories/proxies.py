from sqlalchemy import and_

from app.models.proxy import Proxy
from app.utils.repository import SQLAlchemyRepository


class ProxiesRepository(SQLAlchemyRepository):
    model = Proxy

    async def take(self, proxy_id: int):
        await self.update({"busy": True}, self.model.id == proxy_id)

    async def release(self, proxy_id: int):
        await self.update({"busy": False}, self.model.id == proxy_id)

    async def find_by_id(self, proxy_id: int):
        return await self.find_one(self.model.id == proxy_id)

    async def work_true(self, proxy_id: int):
        await self.update({"work": True}, self.model.id == proxy_id)

    async def work_false(self, proxy_id: int):
        await self.update({"work": False}, self.model.id == proxy_id)

    async def find_for_working(self):
        proxies = await self.find_all(
            and_(self.model.busy.is_(False), self.model.work.is_(True))
        )
        return proxies

    async def find_non_working(self):
        proxies = await self.find_all(self.model.work.is_(False))
        return proxies
