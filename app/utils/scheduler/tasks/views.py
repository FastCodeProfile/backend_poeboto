import asyncio

from loguru import logger

from app.models.proxy import Proxy
from app.models.tasks import ViewsTasks
from app.repositories.bots import BotsRepository
from app.repositories.proxies import ProxiesRepository
from app.repositories.tasks import ViewsTasksRepository
from app.services.bots import BotsService
from app.services.proxies import ProxiesService
from app.services.tasks import TasksService
from app.utils.telegram.client import Telegram


class Views:
    bots_service = BotsService(BotsRepository)
    proxies_service = ProxiesService(ProxiesRepository)
    tasks_service = TasksService(ViewsTasksRepository)

    async def run_tasks(self, ctx):
        tasks = []
        proxies = await self.proxies_service.get_proxies_for_working()
        if not proxies:
            logger.warning("Сейчас нет свободных прокси, задача просмотры")
            return

        tasks_pending = await self.tasks_service.get_tasks_pending()
        for task_pending, proxy in zip(tasks_pending, proxies):
            tasks.append(
                asyncio.create_task(self.execution_tasks(
                    task_pending, proxy
                ))
            )
        await asyncio.gather(*tasks)

    async def execution_tasks(self, this_task: ViewsTasks, proxy: Proxy):
        this_task.in_progress = True
        await self.tasks_service.update_task(this_task.to_read_model())
        await self.proxies_service.proxies_repo.take(proxy.id)
        logger.info(f"Выполняю задачу №{this_task.id}, накрутка просмотров.")

        for bot in await self.bots_service.get_bots_for_working(this_task.skip_bots):
            if (await self.tasks_service.tasks_repo.find_by_id(this_task.id)).pause:
                return

            await self.bots_service.bots_repo.take(bot.id)

            if not await self.proxies_service.rotation(proxy):
                await self.proxies_service.proxies_repo.release(proxy.id)
                return

            await self.tasks_service.update_task(this_task.to_read_model(), bot.id)

            client = Telegram(bot, proxy)
            if not await client.start():
                continue

            try:
                await client.view(this_task.link, this_task.limit)
                this_task.count_done += 1
                await self.tasks_service.update_task(this_task.to_read_model())

            except Exception as err:
                logger.error(f"Ошибка при выполнении задачи #{this_task.id}: {err}")
                this_task.in_progress = False
                await self.proxies_service.proxies_repo.release(proxy.id)
                await self.tasks_service.update_task(this_task.to_read_model())
                return

            finally:
                await self.bots_service.bots_repo.release(bot.id)
                await client.stop()
                if this_task.count <= this_task.count_done:
                    logger.success(f"Задача №{this_task.id}. Выполнено.")
                    this_task.completed = True
                    this_task.in_progress = False
                    await self.proxies_service.proxies_repo.release(proxy.id)
                    await self.tasks_service.update_task(this_task.to_read_model())
                    return

        this_task.in_progress = False
        await self.proxies_service.proxies_repo.release(proxy.id)
        await self.tasks_service.update_task(this_task.to_read_model())
        logger.success(f"Задача №{this_task.id}, не хватило ботов для выполнения.")

