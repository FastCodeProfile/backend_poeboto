from httpx import AsyncClient, ReadTimeout, ConnectTimeout, ConnectError

from app.repositories.proxies import ProxiesRepository
from app.schemas.proxies import ProxySchemaAdd


class ProxiesService:
    def __init__(self, proxies_repo: ProxiesRepository):
        self.proxies_repo: ProxiesRepository = proxies_repo()

    async def add_proxy(self, proxy: ProxySchemaAdd):
        proxy_dict = proxy.model_dump()
        proxy_id = await self.proxies_repo.add_one(proxy_dict)
        proxy = await self.proxies_repo.find_by_id(proxy_id)
        return proxy.to_read_model()

    async def get_proxies_for_working(self):
        working_proxies = []
        proxies = await self.proxies_repo.find_for_working()
        for proxy in proxies:
            if await self.rotation(proxy):
                working_proxies.append(proxy)

        return working_proxies

    async def rotation(self, proxy) -> bool:
        try:
            async with AsyncClient(timeout=30) as async_client:
                await async_client.get(proxy.rotation_url)
                return True
        except (ReadTimeout, ConnectTimeout, ConnectError):
            await self.proxies_repo.work_false(proxy.id)

    async def get_proxies_non_working(self):
        proxies = await self.proxies_repo.find_non_working()
        return proxies
