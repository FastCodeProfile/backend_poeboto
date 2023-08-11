from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[bool] = mapped_column(Integer(), default=False)
    task_name: Mapped[str] = mapped_column(String(), default=False)
    link: Mapped[int] = mapped_column(String(), nullable=False)
    photo: Mapped[str] = mapped_column(String(), default=False)
