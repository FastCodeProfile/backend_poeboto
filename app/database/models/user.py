from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from . import ViewsTask, SubscribersTask


class User(Base):
    balance: Mapped[str] = mapped_column(sa.Float, unique=False, default=0.00)
    username: Mapped[str] = mapped_column(sa.Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=False)
    views: Mapped[list["ViewsTask"]] = orm.relationship(back_populates="user", uselist=True, lazy="joined")
    subscribers: Mapped[list["SubscribersTask"]] = orm.relationship(back_populates="user", uselist=True, lazy="joined")

    def __repr__(self):
        return f"User:{self.id=}"
