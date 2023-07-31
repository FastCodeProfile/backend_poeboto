from app.repositories.tasks import TasksRepository


class TasksService:
    def __init__(self, tasks_repo: TasksRepository):
        self.tasks_repo: TasksRepository = tasks_repo()

    async def add_task(self, task, user_id: int, url_avatar: str):
        existing_task = await self.tasks_repo.find_existing_task(task.link)
        if existing_task:
            existing_task = existing_task.to_read_model()
            existing_task.count += task.count
            existing_task.in_progress = False
            existing_task.completed = False
            if hasattr(task, "limit"):
                existing_task.limit += task.limit
            await self.update_task(existing_task)
            return existing_task
        else:
            task_dict = task.model_dump()
            task_dict["url_avatar"] = url_avatar
            task_dict["user_id"] = user_id
            task_id = await self.tasks_repo.add_one(task_dict)
            task = await self.tasks_repo.find_by_id(task_id)
            return task.to_read_model()

    async def get_tasks(self):
        tasks = await self.tasks_repo.find_all()
        return tasks

    async def update_task(self, task, skip_bots: int = None):
        task_dict = task.model_dump()
        if skip_bots:
            task_dict["skip_bots"] = skip_bots

        await self.tasks_repo.update_task(task_dict)

    async def get_tasks_user(self, user_id: int):
        tasks = await self.tasks_repo.find_tasks_user(user_id)
        return tasks

    async def get_tasks_user_pending(self, user_id: int):
        tasks = await self.tasks_repo.find_tasks_user_pending(user_id)
        return tasks

    async def get_tasks_pending(self):
        tasks = await self.tasks_repo.find_tasks_pending()
        return tasks

    async def get_tasks_user_in_progress(self, user_id: int):
        tasks = await self.tasks_repo.find_tasks_user_in_progress(user_id)
        return tasks

    async def get_tasks_user_completed(self, user_id: int):
        tasks = await self.tasks_repo.find_tasks_user_completed(user_id)
        return tasks
