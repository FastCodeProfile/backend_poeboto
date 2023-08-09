from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class BaseTask(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    link: Mapped[str] = mapped_column(String(), nullable=False)
    pause: Mapped[bool] = mapped_column(Boolean(), default=False)
    avatar: Mapped[str] = mapped_column(String(), nullable=False)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    count_done: Mapped[int] = mapped_column(Integer(), default=0)
    start_date = mapped_column(DateTime(), nullable=False)
    end_date = mapped_column(DateTime(), nullable=False)
    next_start_date = mapped_column(DateTime(), nullable=False)
    done_in_hour = mapped_column(Integer(), default=0)

    def limit_in_hour(self):
        hours = int((self.end_date - self.start_date).total_seconds() / 60 / 60)
        limit_in_hour = int(self.count / hours)
        return limit_in_hour or 1
