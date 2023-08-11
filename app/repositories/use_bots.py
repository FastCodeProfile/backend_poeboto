from sqlalchemy import and_

from app.models.use_bots import UseBots
from app.utils.repository import SQLAlchemyRepository


class UseBotsRepo(SQLAlchemyRepository):
    model = UseBots

    async def find_existing(self, chat_id: str, bot_id: int) -> bool:
        use_bot = await self.find_one(
            and_(
                self.model.bot_id == bot_id,
                self.model.chat_id == chat_id
            )
        )
        return bool(use_bot)
