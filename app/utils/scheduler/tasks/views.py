from datetime import timedelta

from loguru import logger

from app.core import deps
from app.models.tasks import ViewsTasks
from app.repositories.skip_bots import SkipBotsRepository
from app.services.skip_bots import SkipBotsService

from .abc import ABCTasks


class Views(ABCTasks):
    tasks_service = deps.views_tasks_service()
    skip_bots_service = SkipBotsService(SkipBotsRepository)

    async def execution(self, this_task: ViewsTasks):
        logger.info(f"Выполняю задачу №{this_task.id}, накрутка просмотров.")

        if this_task.completed_in_hour >= this_task.limit_in_hour():
            this_task.completed_in_hour = 0
            this_task.next_start_date += timedelta(hours=1)
            await self.tasks_service.update_task(this_task.to_read_model())
            logger.info(f"Задача №{this_task.id}. Достигло часового лимита.")
            return

        try:
            await self.client.view(this_task.link, this_task.limit)
            this_task.count_done += 1
            this_task.completed_in_hour += 1
            await self.skip_bots_service.add_skip_bots(
                this_task.name, this_task.id, self.bot_id
            )
            await self.tasks_service.update_task(this_task.to_read_model())

        except Exception as err:
            logger.error(f"Ошибка при выполнении задачи №{this_task.id}: {err}")

        finally:
            if this_task.count <= this_task.count_done:
                logger.success(f"Задача №{this_task.id}. Выполнено.")
