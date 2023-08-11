import asyncio
from random import shuffle

from loguru import logger

from app.core import deps
from app.models.bots import Bots
from app.models.proxies import Proxies
from app.utils.telegram.client import Telegram
from ..tasks.subscribers import Subscribers
from ..tasks.views import Views


class RunTasks:
    bots_service = deps.bots_service()
    proxies_service = deps.proxies_service()
    views_service = deps.views_service()
    subscribers_service = deps.subscribers_service()

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
            subscribers_tasks = await self.subscribers_service.get_tasks_for_working(bot.id)
            views_tasks = await self.views_service.get_tasks_for_working(bot.id)
            tg_tasks = subscribers_tasks + views_tasks
            if not tg_tasks:
                await self.bots_service.bots_repo.release(bot.id)
                await self.proxies_service.proxies_repo.release(proxy.id)
                await self.bots_service.update_bot(bot.to_read_model(), last_call=True)
                logger.warning(f"Для бота №{bot.id}, нет задач для работы.")
                continue
            else:
                shuffle(tg_tasks)
                for task in tg_tasks:
                    if task.task == "subscribers":
                        await self.subscribers_service.tasks_repo.take(task.id)

                    if task.task == "views":
                        await self.views_service.tasks_repo.take(task.id)

                tasks.append(asyncio.create_task(self.execution_tasks(bot, proxy, tg_tasks)))

        await asyncio.gather(*tasks)

    async def execution_tasks(self, bot: Bots, proxy: Proxies, tasks):
        client = Telegram(bot.to_read_model(), proxy)
        if not await client.start():
            await self.bots_service.bots_repo.release(bot.id)
            await self.proxies_service.proxies_repo.release(proxy.id)
            return

        for task in tasks:
            if task.pause:
                continue

            if task.task == "subscribers":
                await Subscribers(client, bot.id).execution(task)
                await self.subscribers_service.tasks_repo.release(task.id)

            if task.task == "views":
                await Views(client, bot.id).execution(task)
                await self.views_service.tasks_repo.release(task.id)

        await self.bots_service.bots_repo.release(bot.id)
        await self.proxies_service.proxies_repo.release(proxy.id)
