from datetime import datetime, timedelta

from loguru import logger

from app.core import deps
from app.models.tasks.subscribers import SubscribersTask
from app.services.chats import ChatsService, ChatsRepo
from .abc import ABCTasks


class Multiple(ABCTasks):
    tasks_service = deps.multiple_service()
    chats_service = ChatsService(ChatsRepo)

    async def execution(self, this_task: SubscribersTask):
        logger.info(f"Выполняю задачу №{this_task.id}, множественная.")

        try:
            chats = await self.chats_service.get_chats_by_task(this_task.task, this_task.id)
            for chat in chats:
                await self.client.subscribe(chat.link)
                this_task.last_date_start = datetime.now() + timedelta(seconds=this_task.delay)
                await self.use_bots_service.add_use_bot(chat.id, self.bot_id)
                await self.tasks_service.update_task(this_task.to_read_model())
            this_task.count_done += 1

        except Exception as err:
            logger.error(f"Ошибка при выполнении задачи №{this_task.id}: {err}")

        finally:
            if this_task.count <= this_task.count_done:
                logger.success(f"Задача №{this_task.id}. Выполнено.")
