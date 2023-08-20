from random import shuffle

from loguru import logger

from app.core import depends
from app.db import Database
from app.db.models import ViewsTask, SubscribersTask
from app.utils.telegram.client import Telegram


class RunTasks:
    db: Database

    async def init_db(self):
        self.db = await depends.get_db()

    async def get_bots(self) -> list[Telegram]:
        bots = await self.db.bot.get_for_working()
        proxy = await self.db.proxy.get_for_working()
        bots_ = []
        for bot, proxy_ in zip(bots, proxy):
            await self.db.bot.update(bot.id, busy=True)
            await self.db.proxy.update(proxy_.id, busy=True)
            await self.db.session.commit()
            client = Telegram(bot, proxy_)
            if await client.start():
                bots_.append(client)
            else:
                await self.db.bot.update(bot.id, busy=False, ban=True)
                await self.db.proxy.update(proxy_.id, busy=False)
                await self.db.session.commit()
        return bots_

    async def get_tasks(self):
        views_tasks = await self.db.views_task.get_for_working()
        subscribers_tasks = await self.db.subscribers_task.get_for_working()
        tasks = views_tasks + subscribers_tasks
        shuffle(tasks)
        return tasks

    async def run_tasks(self, ctx):
        await self.init_db()
        bots = await self.get_bots()
        if not bots:
            logger.info("Нет свободных ботов или прокси для работы.")

        tasks = await self.get_tasks()
        if not tasks:
            logger.info("Нет задач для выполнения.")

        for bot in bots:
            for task in tasks:
                if isinstance(task, ViewsTask):
                    try:
                        await self.db.views_task.update(task.id, busy=True)
                        await self.db.session.commit()
                        for target in task.targets:
                            if bot.bot.id not in [used_bot.id for used_bot in target.used_bots]:
                                await bot.view(target.target, task.limit)
                                await self.db.views_target.update(target.id, count_done=target.count_done+1)
                                await self.db.session.commit()
                                logger.info(f"Просмотры: задача №{task.id} - {target.count}/{target.count_done}")
                            else:
                                continue
                    finally:
                        await self.db.views_task.update(task.id, busy=False)
                        await self.db.session.commit()
                if isinstance(task, SubscribersTask):
                    try:
                        await self.db.subscribers_task.update(task.id, busy=True)
                        await self.db.session.commit()
                        for target in task.targets:
                            if bot.bot.id not in [used_bot.id for used_bot in target.used_bots]:
                                await bot.subscribe(target.target)
                                await self.db.views_target.update(target.id, count_done=target.count_done+1)
                                await self.db.session.commit()
                                logger.info(f"Подписчики: задача №{task.id} - {target.count}/{target.count_done}")
                            else:
                                continue
                    finally:
                        await self.db.subscribers_task.update(task.id, busy=False)
                        await self.db.session.commit()

            await self.db.bot.update(bot.bot.id, busy=False)
            await self.db.session.commit()
