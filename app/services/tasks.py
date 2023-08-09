from app.repositories.skip_bots import SkipBotsRepository
from app.repositories.tasks.base import TasksRepo
from app.services.skip_bots import SkipBotsService


class TasksService:
    def __init__(self, tasks_repo: TasksRepo):
        self.tasks_repo: TasksRepo = tasks_repo()

    async def add_task(self, task, user_id: int, avatar: str):
        existing_task = await self.tasks_repo.find_task_existing(task.link)
        if existing_task:
            existing_task = existing_task.to_read_model()
            existing_task.count += task.count
            existing_task.start_date = task.start_date
            existing_task.end_date = task.end_date
            existing_task.next_start_date = task.start_date
            if hasattr(task, "limit"):
                existing_task.limit += task.limit
            await self.update_task(existing_task)
            return existing_task
        else:
            task_dict = task.model_dump()
            task_dict["avatar"] = avatar
            task_dict["user_id"] = user_id
            task_dict["next_start_date"] = task.start_date
            task_id = await self.tasks_repo.add_one(task_dict)
            task = await self.tasks_repo.find_task_by_id(task_id)
            return task.to_read_model()

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
