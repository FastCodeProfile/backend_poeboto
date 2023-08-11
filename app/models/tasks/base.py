from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class BaseTask(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pause: Mapped[bool] = mapped_column(Boolean(), default=False)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    count_done: Mapped[int] = mapped_column(Integer(), default=0)
    start_date = mapped_column(DateTime(), nullable=False)
    last_date_start = mapped_column(DateTime(), nullable=False)
    end_date = mapped_column(DateTime(), nullable=False)
    delay: Mapped[int] = mapped_column(Integer(), default=0)
    busy: Mapped[bool] = mapped_column(Boolean(), default=False)
