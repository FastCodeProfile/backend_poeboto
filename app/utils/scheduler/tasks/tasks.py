import asyncio
from random import shuffle

from loguru import logger

from app.models.bots import Bots
from app.models.proxy import Proxy
from app.repositories.bots import BotsRepository
from app.repositories.proxies import ProxiesRepository
from app.repositories.tasks import ViewsTasksRepository, SubscribersTasksRepository
from app.services.bots import BotsService
from app.services.proxies import ProxiesService
from app.services.tasks import TasksService


class Tasks:
    bots_service = BotsService(BotsRepository)
    proxies_service = ProxiesService(ProxiesRepository)
    views_tasks_service = TasksService(ViewsTasksRepository)
    subscribers_tasks_service = TasksService(SubscribersTasksRepository)

    async def run_tasks(self, ctx):
        tasks = []
        bots = await self.bots_service.get_bots_for_working()
        proxies = await self.proxies_service.get_proxies_for_working()
        if not proxies:
            logger.warning("Сейчас нет свободных прокси, задача просмотры")
            return

        for bot, proxy in zip(bots, proxies):
            tasks.append(
                asyncio.create_task(self.execution_tasks(
                    bot, proxy
                ))
            )
        await asyncio.gather(*tasks)

    async def execution_tasks(self, bot: Bots, proxy: Proxy):
        views_tasks = await self.views_tasks_service.get_tasks_pending()
        subscribers_tasks = await self.subscribers_tasks_service.get_tasks_pending()
        tasks = views_tasks+subscribers_tasks
        logger.success(tasks)
        shuffle(tasks)
        for task in tasks:
            logger.info(task)
