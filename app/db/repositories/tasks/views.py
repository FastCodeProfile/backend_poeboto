from datetime import datetime
from typing import Sequence

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..abstract import Repository
from ...models import ViewsTask, ViewsTarget, ViewsUsedBot


class ViewsTaskRepo(Repository[ViewsTask]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=ViewsTask, session=session)

    async def new(
        self,
        user_fk: id,
        count: int,
        start_date: datetime,
        end_date: datetime,
        limit: int,
        targets: list["ViewsTarget"] = []
    ) -> ViewsTask:
        delay = int((end_date - start_date).total_seconds() / count)
        new_task = await self.session.merge(
            ViewsTask(
                user_fk=user_fk,
                start_date=start_date,
                end_date=end_date,
                next_start_date=start_date,
                delay=delay,
                limit=limit,
                targets=targets
            )
        )
        return new_task

    async def get_for_working(self) -> list[ViewsTask]:
        tasks = await self.get_many(and_(
            ViewsTask.busy.is_(False),
            ViewsTask.pause.is_(False),
            ViewsTask.completed.is_(False)
        ))
        return tasks


class ViewsTargetRepo(Repository[ViewsTarget]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=ViewsTarget, session=session)

    async def new(
        self,
        task_fk: int,
        count: int,
        target: str,
    ) -> ViewsTarget:
        new_target = await self.session.merge(
            ViewsTarget(
                count=count,
                task_fk=task_fk,
                target=target,
                photo="надо сделать"
            )
        )
        return new_target


class ViewsUsedBotRepo(Repository[ViewsUsedBot]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=ViewsUsedBot, session=session)

    async def new(
        self,
        bot_fk: int,
        count: int,
        target_fk: int,
    ) -> ViewsUsedBot:
        new_used_bot = await self.session.merge(
            ViewsUsedBot(
                count=count,
                bot_fk=bot_fk,
                target_fk=target_fk,
            )
        )
        return new_used_bot
