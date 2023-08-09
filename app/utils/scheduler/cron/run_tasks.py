import asyncio
from random import shuffle

from loguru import logger

from app.core import deps
from app.models.bots import Bots
from app.models.proxy import Proxy
from app.utils.telegram.client import Telegram

from ..tasks.subscribers import Subscribers
from ..tasks.views import Views


class RunTasks:
    bots_service = deps.bots_service()
    proxies_service = deps.proxies_service()
    views_tasks_service = deps.views_tasks_service()
    subscribers_tasks_service = deps.subscribers_tasks_service()

    async def run_tasks(self, ctx):
        bots = await self.bots_service.get_bots_for_working()
        if not bots:
            logger.warning("Сейчас нет свободных ботов.")
            return

        proxies = await self.proxies_service.get_proxies_for_working()
        if not proxies:
            logger.warning("Сейчас нет свободных прокси.")
            return

        tasks = []

        for bot, proxy in zip(bots, proxies):
            await self.bots_service.bots_repo.take(bot.id)
            await self.proxies_service.proxies_repo.take(proxy.id)
            tasks.append(asyncio.create_task(self.execution_tasks(bot, proxy)))

        await asyncio.gather(*tasks)

    async def execution_tasks(self, bot: Bots, proxy: Proxy):
        subscribers_tasks = await self.subscribers_tasks_service.get_tasks_for_working(
            bot.id
        )
        views_tasks = await self.views_tasks_service.get_tasks_for_working(bot.id)
        tasks = subscribers_tasks + views_tasks
        if not tasks:
            await self.bots_service.bots_repo.release(bot.id)
            await self.proxies_service.proxies_repo.release(proxy.id)
            logger.warning("Сейчас нет задач для работы")
            return
        shuffle(tasks)

        client = Telegram(bot.to_read_model(), proxy)
        if not await client.start():
            await self.bots_service.bots_repo.release(bot.id)
            await self.proxies_service.proxies_repo.release(proxy.id)
            return

        for task in tasks:
            if task.pause:
                continue

            if task.name == "subscribers":
                await Subscribers(client, bot.id).execution(task)

            if task.name == "views":
                await Views(client, bot.id).execution(task)

        await self.bots_service.bots_repo.release(bot.id)
        await self.proxies_service.proxies_repo.release(proxy.id)
