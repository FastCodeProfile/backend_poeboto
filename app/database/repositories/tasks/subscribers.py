from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.telegram import get_target_photo
from ..abstract import Repository
from ...models import SubscribersTask, SubscribersTarget, SubscribersUsedBot


class SubscribersTaskRepo(Repository[SubscribersTask]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=SubscribersTask, session=session)

    async def new(
        self,
        user_fk: int,
        count: int,
        start_date: datetime,
        end_date: datetime,
        targets: list["SubscribersTarget"] = []
    ) -> SubscribersTask:
        delay = int((end_date - start_date).total_seconds() / count)
        new_task = await self.session.merge(
            SubscribersTask(
                user_fk=user_fk,
                start_date=start_date,
                end_date=end_date,
                next_start_date=start_date,
                delay=delay,
                targets=targets
            )
        )
        return new_task

    async def get_for_working(self) -> list[SubscribersTask]:
        tasks = await self.get_many(and_(
            SubscribersTask.busy.is_(False),
            SubscribersTask.pause.is_(False),
            SubscribersTask.completed.is_(False),
            SubscribersTask.next_start_date <= datetime.now()
        ))
        return tasks


class SubscribersTargetRepo(Repository[SubscribersTarget]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=SubscribersTarget, session=session)

    async def new(
        self,
        task_fk: int,
        count: int,
        target: str,
    ) -> SubscribersTarget:
        photo = await get_target_photo(target)
        new_target = await self.session.merge(
            SubscribersTarget(
                count=count,
                task_fk=task_fk,
                target=target,
                photo=photo
            )
        )
        return new_target

    async def get_for_working(self) -> list[SubscribersTarget]:
        targets = await self.get_many(and_(
            SubscribersTarget.count > SubscribersTarget.count_done,
        ))
        return targets


class SubscribersUsedBotRepo(Repository[SubscribersUsedBot]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=SubscribersUsedBot, session=session)

    async def new(
        self,
        bot_fk: int,
        target_fk: int,
    ) -> SubscribersUsedBot:
        new_used_bot = await self.session.merge(
            SubscribersUsedBot(
                bot_fk=bot_fk,
                target_fk=target_fk,
            )
        )
        return new_used_bot
