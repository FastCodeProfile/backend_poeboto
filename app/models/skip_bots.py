from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class SkipBots(Base):
    __tablename__ = "skip_bots"

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    task_id: Mapped[bool] = mapped_column(Integer(), default=False)
    task_name: Mapped[str] = mapped_column(String(), default=False)
