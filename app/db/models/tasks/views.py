from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from .abstract import AbstractTask, AbstractTarget
from ..base import Base

if TYPE_CHECKING:
    from .. import User


class ViewsTask(AbstractTask):
    user: Mapped["User"] = orm.relationship(back_populates='views', uselist=False)
    targets: Mapped[list["ViewsTarget"]] = orm.relationship(back_populates="task", uselist=True, lazy="joined")
    limit: Mapped[int] = mapped_column(sa.Integer, default=1)

    def __repr__(self):
        return f"ViewsTask:{self.id=}"


class ViewsTarget(AbstractTarget):
    task: Mapped["ViewsTask"] = orm.relationship(back_populates='targets', uselist=False)
    task_fk: Mapped[int] = mapped_column(sa.ForeignKey('viewstask.id', ondelete='CASCADE'), unique=False, nullable=False)
    used_bots: Mapped[list["ViewsUsedBot"]] = orm.relationship(back_populates="target", uselist=True, lazy="joined")

    def __repr__(self):
        return f"ViewsTarget:{self.id=}"


class ViewsUsedBot(Base):
    bot_fk: Mapped[int] = mapped_column(sa.ForeignKey('bot.id', ondelete='CASCADE'), unique=False, nullable=False)
    target_fk: Mapped[int] = mapped_column(sa.ForeignKey('viewstarget.id', ondelete='CASCADE'), unique=False, nullable=False)
    target: Mapped["ViewsTarget"] = orm.relationship(back_populates='used_bots', uselist=False)

    def __repr__(self):
        return f"ViewsUsedBot:{self.id=}"
