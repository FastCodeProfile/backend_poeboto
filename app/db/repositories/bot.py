from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models import Bot


class BotRepo(Repository[Bot]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Bot, session=session)

    async def new(
        self,
        api_id: int,
        api_hash: str,
        password: str,
        lang_code: str,
        app_version: str,
        device_model: str,
        session_string: str,
    ) -> Bot:
        new_bot = await self.session.merge(
            Bot(
                api_id=api_id,
                api_hash=api_hash,
                password=password,
                lang_code=lang_code,
                app_version=app_version,
                device_model=device_model,
                session_string=session_string
            )
        )
        return new_bot

    async def get_for_working(self):
        bots = await self.get_many(and_(
            Bot.ban.is_(False),
            Bot.busy.is_(False),
        ), limit=10, order_by=Bot.last_call)
        return bots
