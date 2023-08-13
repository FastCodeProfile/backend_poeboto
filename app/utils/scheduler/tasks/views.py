from datetime import datetime, timedelta

from loguru import logger

from app.core import deps
from app.models.tasks.views import ViewsTask
from app.services.chats import ChatsService, ChatsRepo
from .abc import ABCTasks


class Views(ABCTasks):
    tasks_service = deps.views_service()
    chats_service = ChatsService(ChatsRepo)

    async def execution(self, this_task: ViewsTask):
        logger.info(f"Задача №{this_task.id}, накрутка просмотров. - Выполняю...")

        try:
            chats = await self.chats_service.get_chats_by_task(this_task.task, this_task.id)
            for chat in chats:
                logger.info(f"Задача №{this_task.id}, накрутка просмотров. - Просмотров, бот №{self.bot_id}")
                await self.client.view(chat.link, this_task.limit)
                this_task.last_date_start += timedelta(seconds=this_task.delay)
                await self.use_bots_service.add_use_bot(chat.id, self.bot_id)

            this_task.count_done += 1
            await self.tasks_service.update_task(this_task.to_read_model())

        except Exception as err:
            logger.error(f"Задача №{this_task.id}, накрутка просмотров. - Ошибка: {err}")

        finally:
            if this_task.count <= this_task.count_done:
                logger.success(f"Задача №{this_task.id}, накрутка просмотров. - Выполнено.")
