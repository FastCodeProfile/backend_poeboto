from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class AbstractTask(Base):
    __abstract__ = True

    user_fk: Mapped[int] = mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'), unique=False, nullable=False)
    pause: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    start_date: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    next_start_date: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    delay: Mapped[int] = mapped_column(sa.Integer, default=0)
    busy: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    completed: Mapped[bool] = mapped_column(sa.Boolean, default=False)


class AbstractTarget(Base):
    __abstract__ = True

    error: Mapped[str] = mapped_column(sa.String, nullable=True)
    count: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    count_done: Mapped[int] = mapped_column(sa.Integer, default=0)
    target: Mapped[str] = mapped_column(sa.String, nullable=False)
    photo: Mapped[str] = mapped_column(sa.String, nullable=False)
