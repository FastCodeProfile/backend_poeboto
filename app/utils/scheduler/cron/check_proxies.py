import asyncio

from loguru import logger

from app.repositories.proxies import ProxiesRepository
from app.services.proxies import ProxiesService


async def check_proxy(proxies_service: ProxiesService, proxy):
    logger.info(f"Проверяю прокси №{proxy.id}.")
    if await proxies_service.rotation(proxy):
        await proxies_service.proxies_repo.work_true(proxy.id)


async def run_check_proxies(ctx):
    tasks = []
    proxies_service = ProxiesService(ProxiesRepository)
    for proxy in await proxies_service.get_proxies_non_working():
        task = asyncio.create_task(check_proxy(proxies_service, proxy))
        tasks.append(task)

    await asyncio.gather(*tasks)
