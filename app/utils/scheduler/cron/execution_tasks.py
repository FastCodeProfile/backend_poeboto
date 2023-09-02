import datetime
import itertools
from random import shuffle

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Database
from app.database.database import engine
from app.database.models import ViewsTask, SubscribersTask
from app.utils.scheduler.tasks import views, subscribes
from app.utils.telegram.client import TgClient


async def get_tasks(db: Database) -> list[ViewsTask | SubscribersTask]:
    tasks = []
    views_tasks = await db.views_task.get_for_working()
    for task in views_tasks:
        await db.views_task.update(task.id, busy=True)
        await db.session.commit()
        tasks.append(task)
    subscribers_tasks = await db.subscribers_task.get_for_working()
    for task in subscribers_tasks:
        await db.subscribers_task.update(task.id, busy=True)
        await db.session.commit()
        tasks.append(task)
    shuffle(tasks)
    return tasks


async def get_clients(db: Database) -> list[TgClient]:
    clients = []
    proxies = await db.proxy.get_for_working()
    bot_generator = itertools.chain(await db.bot.get_for_working())
    for proxy in proxies:
        await db.proxy.update(proxy.id, busy=True)
        await db.session.commit()
        client = TgClient(bot_generator, db)
        if await client.start(proxy):
            clients.append(client)
        await db.bot.update(client.bot_id, last_call=datetime.datetime.now())
        await db.session.commit()
    return clients


async def execution_tasks(ctx):
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        completed_tasks = []
        db = Database(session)
        tasks = await get_tasks(db)
        if not tasks:
            logger.info("Нет задач для выполнения.")
        else:
            clients = await get_clients(db)
            if not clients:
                logger.info("Нет свободных ботов или прокси для работы.")
            else:
                for client in clients:
                    for task in tasks:
                        if task not in completed_tasks:
                            if isinstance(task, ViewsTask):
                                await views(db, task, client)
                                completed_tasks.append(task)
                            if isinstance(task, SubscribersTask):
                                await subscribes(db, task, client)
                                completed_tasks.append(task)

                    await db.bot.update(client.bot_id, busy=False)
                    await db.proxy.update(client.proxy_id, busy=False)
                    await db.session.commit()
