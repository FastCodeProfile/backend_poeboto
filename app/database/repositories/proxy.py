from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, TimeoutException

from .abstract import Repository
from ..models import Proxy


class ProxyRepo(Repository[Proxy]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Proxy, session=session)

    async def new(
        self,
        url: str,
        ip: str,
        port: int,
        scheme: str,
        username: str,
        password: str,
    ) -> Proxy:
        new_proxy = await self.session.merge(
            Proxy(
                url=url,
                ip=ip,
                port=port,
                scheme=scheme,
                username=username,
                password=password,
            )
        )
        return new_proxy

    async def get_for_working(self) -> list[Proxy]:
        proxies = await self.get_many(and_(
            Proxy.working.is_(True),
            Proxy.busy.is_(False),
        ), limit=10)
        proxies_ = []
        for proxy in proxies:
            try:
                await self.update(proxy.id, busy=True)
                await self.session.commit()
                async with AsyncClient(timeout=40) as client:
                    await client.get(proxy.url)
                proxies_.append(proxy)
            except TimeoutException:
                await self.update(proxy.id, working=False, busy=False)
                await self.session.commit()
        return proxies_
