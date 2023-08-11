from datetime import datetime, timedelta

from sqlalchemy import and_

from app.utils.repository import SQLAlchemyRepository


class TasksRepo(SQLAlchemyRepository):
    model = None

    async def take(self, task_id: int):
        await self.update({"busy": True}, self.model.id == task_id)

    async def release(self, task_id: int):
        await self.update({"busy": False}, self.model.id == task_id)

    async def update_task(self, task):
        task_dict = task.model_dump()
        await self.update(task_dict, self.model.id == task.id)

    async def find_task_by_id(self, task_id: int):
        task = await self.find_one(self.model.id == task_id)
        return task

    async def find_tasks_user(self, user_id: int):
        tasks = await self.find_all(self.model.user_id == user_id)
        return tasks

    async def find_tasks_for_working(self):
        tasks = await self.find_all(
            and_(
                self.model.pause.is_(False),
                self.model.busy.is_(False),
                self.model.count > self.model.count_done,
                self.model.start_date <= datetime.now(),
                self.model.last_date_start <= datetime.now(),
            )
        )
        return tasks
