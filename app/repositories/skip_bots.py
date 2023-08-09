from sqlalchemy import and_

from app.models.skip_bots import SkipBots
from app.utils.repository import SQLAlchemyRepository


class SkipBotsRepository(SQLAlchemyRepository):
    model = SkipBots

    async def find_existing(self, task_name: str, task_id: int, bot_id: int) -> bool:
        task = await self.find_one(
            and_(
                self.model.task_name == task_name,
                self.model.task_id == task_id,
                self.model.bot_id == bot_id,
            )
        )
        return bool(task)
