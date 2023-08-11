from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from .chats import Chats


class UseBots(Base):
    __tablename__ = "use_bots"

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    chat_id: Mapped[Chats.id] = mapped_column(ForeignKey("chats.id"))
