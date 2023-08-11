from app.services.use_bots import UseBotsService, UseBotsRepo
from app.services.chats import ChatsService, ChatsRepo


class BaseService:
    tasks_repo: None

    async def get_tasks(self):
        tasks = await self.tasks_repo.find_all()
        return tasks

    async def update_task(self, task):
        await self.tasks_repo.update_task(task)

    async def get_tasks_user(self, user_id: int):
        tasks = await self.tasks_repo.find_tasks_user(user_id)
        return tasks

    async def get_tasks_for_working(self, bot_id: int):
        tasks_for_working = []
        tasks = await self.tasks_repo.find_tasks_for_working()
        for task in tasks:
            chats_service = ChatsService(ChatsRepo)
            chats = await chats_service.get_chats_by_task(task.task, task.id)
            use_bots_service = UseBotsService(UseBotsRepo)
            for chat in chats:
                if not await use_bots_service.existing(chat.id, bot_id):
                    tasks_for_working.append(task)
                    break

        return tasks_for_working
