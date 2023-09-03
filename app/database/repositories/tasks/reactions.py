from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.telegram import get_target_photo
from ..abstract import Repository
from ...models import ReactionsTask, ReactionsTarget, ReactionsUsedBot


class ReactionsTaskRepo(Repository[ReactionsTask]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=ReactionsTask, session=session)

    async def new(
        self,
        user_fk: id,
        count: int,
        reactions: str,
        start_date: datetime,
        end_date: datetime,
        targets: list["ReactionsTarget"] = []
    ) -> ReactionsTask:
        delay = int((end_date - start_date).total_seconds() / count)
        new_task = await self.session.merge(
            ReactionsTask(
                user_fk=user_fk,
                start_date=start_date,
                reactions=reactions,
                end_date=end_date,
                next_start_date=start_date,
                delay=delay,
                targets=targets
            )
        )
        return new_task

    async def get_for_working(self) -> list[ReactionsTask]:
        tasks = await self.get_many(and_(
            ReactionsTask.busy.is_(False),
            ReactionsTask.pause.is_(False),
            ReactionsTask.completed.is_(False),
            ReactionsTask.next_start_date <= datetime.now()
        ))
        return tasks


class ReactionsTargetRepo(Repository[ReactionsTarget]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=ReactionsTarget, session=session)

    async def new(
        self,
        task_fk: int,
        count: int,
        target: str,
    ) -> ReactionsTarget:
        msg_id = target.split("/")[-1]
        photo = await get_target_photo(target.replace(msg_id, ""))
        new_target = await self.session.merge(
            ReactionsTarget(
                count=count,
                task_fk=task_fk,
                target=target,
                photo=photo
            )
        )
        return new_target

    async def get_for_working(self) -> list[ReactionsTarget]:
        targets = await self.get_many(and_(
            ReactionsTarget.count > ReactionsTarget.count_done,
        ))
        return targets


class ReactionsUsedBotRepo(Repository[ReactionsUsedBot]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=ReactionsUsedBot, session=session)

    async def new(
        self,
        bot_fk: int,
        target_fk: int,
    ) -> ReactionsUsedBot:
        new_used_bot = await self.session.merge(
            ReactionsUsedBot(
                bot_fk=bot_fk,
                target_fk=target_fk,
            )
        )
        return new_used_bot
