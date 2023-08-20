from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from .abstract import AbstractTask, AbstractTarget
from ..base import Base

if TYPE_CHECKING:
    from .. import User


class SubscribersTask(AbstractTask):
    user: Mapped["User"] = orm.relationship(back_populates='subscribers', uselist=False)
    targets: Mapped[list["SubscribersTarget"]] = orm.relationship(back_populates="task", uselist=True, lazy="joined")

    def __repr__(self):
        return f"SubscribersTask:{self.id=}"


class SubscribersTarget(AbstractTarget):
    task: Mapped["SubscribersTask"] = orm.relationship(back_populates='targets', uselist=False)
    task_fk: Mapped[int] = mapped_column(sa.ForeignKey('subscriberstask.id', ondelete='CASCADE'), unique=False, nullable=False)
    used_bots: Mapped[list["SubscribersUsedBot"]] = orm.relationship(back_populates="target", uselist=True, lazy="joined")

    def __repr__(self):
        return f"SubscribersTarget:{self.id=}"


class SubscribersUsedBot(Base):
    bot_fk: Mapped[int] = mapped_column(sa.ForeignKey('bot.id', ondelete='CASCADE'), unique=False, nullable=False)
    target_fk: Mapped[int] = mapped_column(sa.ForeignKey('subscriberstarget.id', ondelete='CASCADE'), unique=False, nullable=False)
    target: Mapped["SubscribersTarget"] = orm.relationship(back_populates='used_bots', uselist=False)

    def __repr__(self):
        return f"SubscribersUsedBot:{self.id=}"
