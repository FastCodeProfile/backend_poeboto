from datetime import timedelta

from loguru import logger

from app.core import depends
from app.models.tasks.multiple import MultipleTask
from app.services.chats import ChatsService
from .abc import ABCTasks


class Multiple(ABCTasks):
    tasks_service = depends.multiple_service()
    chats_service = ChatsService()

    async def execution(self, this_task: MultipleTask):
        logger.info(f"Задача №{this_task.id}, множественная. - Выполняю...")

        try:
            chats = await self.chats_service.get_chats_by_task(this_task.task, this_task.id)
            for chat in chats:
                if this_task.count_done <= (int(this_task.count * 0.2) or 1):
                    logger.info(f"Задача №{this_task.id}, множественная. - Просмотры, бот №{self.bot_id}")
                    await self.client.view(chat.link)
                logger.info(f"Задача №{this_task.id}, множественная. - Подписка, бот №{self.bot_id}")
                await self.client.subscribe(chat.link)
                this_task.last_date_start += timedelta(seconds=this_task.delay)
                await self.use_bots_service.add_use_bot(chat.id, self.bot_id)

            this_task.count_done += 1
            await self.tasks_service.update_task(this_task.to_read_model())

        except Exception as err:
            logger.error(f"Задача №{this_task.id}, множественная. - Ошибка: {err}")

        finally:
            if this_task.count <= this_task.count_done:
                logger.success(f"Задача №{this_task.id}, множественная. - Выполнено.")
