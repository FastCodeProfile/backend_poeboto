from sqlalchemy import and_

from app.models.tasks import SubscribersTasks, ViewsTasks
from app.utils.repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    model = None

    async def update_task(self, task):
        await self.update(task, self.model.id == task["id"])

    async def find_by_id(self, task_id: int):
        task = await self.find_one(self.model.id == task_id)
        return task

    async def find_existing_task(self, link: int):
        task = await self.find_one(and_(self.model.link == link))
        return task

    async def find_tasks_user(self, user_id: int):
        tasks = await self.find_all(self.model.user_id == user_id)
        return tasks

    async def find_tasks_pending(self):
        tasks = await self.find_all(
            and_(
                self.model.completed.is_(False),
                self.model.in_progress.is_(False),
                self.model.pause.is_(False),
            )
        )
        return tasks

    async def find_tasks_user_pending(self, user_id: int):
        tasks = await self.find_all(
            and_(
                self.model.completed.is_(False),
                self.model.in_progress.is_(False),
                self.model.user_id == user_id,
            )
        )
        return tasks

    async def find_tasks_user_in_progress(self, user_id: int):
        tasks = await self.find_all(
            and_(
                self.model.completed.is_(False),
                self.model.in_progress.is_(True),
                self.model.user_id == user_id,
            )
        )
        return tasks

    async def find_tasks_user_completed(self, user_id: int):
        tasks = await self.find_all(
            and_(
                self.model.completed.is_(True),
                self.model.in_progress.is_(False),
                self.model.user_id == user_id,
            )
        )
        return tasks


class SubscribersTasksRepository(TasksRepository):
    model = SubscribersTasks


class ViewsTasksRepository(TasksRepository):
    model = ViewsTasks
