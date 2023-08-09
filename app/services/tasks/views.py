from .base import BaseService


class ViewsService(BaseService):
    async def add_task(self, task, user_id: int, avatar: str):
        existing_task = await self.tasks_repo.find_task_existing(task.link)
        if existing_task:
            existing_task = existing_task.to_read_model()
            existing_task.count += task.count
            existing_task.start_date = task.start_date
            existing_task.end_date = task.end_date
            existing_task.next_start_date = task.start_date
            existing_task.limit = task.limit
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
