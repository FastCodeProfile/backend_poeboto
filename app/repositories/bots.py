from datetime import datetime as dt

from sqlalchemy import and_

from app.models.bots import Bots
from app.utils.repository import SQLAlchemyRepository


class BotsRepository(SQLAlchemyRepository):
    model = Bots

    async def update_bot(self, bot):
        bot_dict = bot.model_dump()
        bot_dict["last_call"] = dt.now()
        await self.update(bot_dict, self.model.id == bot.id)

    async def find_by_id(self, bot_id: int):
        bot = await self.find_one(self.model.id == bot_id)
        return bot

    async def find_bots_for_working(self, skip_bots: int):
        bots = await self.find_all(
            and_(
                self.model.ban.is_(False),
                self.model.busy.is_(True),
                self.model.id > skip_bots,
            ),
            self.model.last_call,
        )
        return bots

    async def take(self, bot_id: int):
        await self.update({"busy": True}, self.model.id == bot_id)

    async def release(self, bot_id: int):
        await self.update({"busy": False}, self.model.id == bot_id)
