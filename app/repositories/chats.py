from sqlalchemy import and_

from app.models.chats import Chats
from app.utils.repository import SQLAlchemyRepository


class ChatsRepo(SQLAlchemyRepository):
    model = Chats

    async def find_chats_by_task(self, task_name: str, task_id: int) -> bool:
        chats = await self.find_all(
            and_(
                self.model.task_id == task_id,
                self.model.task_name == task_name,
            )
        )
        return chats

    async def find_chat_by_link(self, link: str) -> bool:
        chats = await self.find_all(
            self.model.link == link,
        )
        return chats
