from app.repositories.skip_bots import SkipBotsRepository
from app.repositories.tasks.base import TasksRepo
from app.services.skip_bots import SkipBotsService


class BaseService:
    def __init__(self, tasks_repo: TasksRepo):
        self.tasks_repo: TasksRepo = tasks_repo()

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
            existing = await SkipBotsService(
                SkipBotsRepository
            ).skip_bots_repo.find_existing(
                task_name=task.name, task_id=task.id, bot_id=bot_id
            )
            if not existing:
                tasks_for_working.append(task)

        return tasks_for_working
