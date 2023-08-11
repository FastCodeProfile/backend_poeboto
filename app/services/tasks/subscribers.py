from datetime import timedelta

from .base import BaseService
from app.repositories.tasks.subscribers import SubscribersRepo


class SubscribersService(BaseService):
    tasks_repo = SubscribersRepo()

    async def add_task(self, task, user_id: int):
        delay = int((task.end_date - task.start_date).total_seconds() / task.count)
        task_dict: dict = task.model_dump()
        task_dict.pop("link")
        task_dict["delay"] = delay
        task_dict["user_id"] = user_id
        task_dict["last_date_start"] = task.start_date
        task_id = await self.tasks_repo.add_one(task_dict)
        task = await self.tasks_repo.find_task_by_id(task_id)
        return task.to_read_model()
