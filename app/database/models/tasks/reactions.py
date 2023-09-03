from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from .abstract import AbstractTask, AbstractTarget
from ..base import Base

if TYPE_CHECKING:
    from .. import User


class ReactionsTask(AbstractTask):
    user: Mapped["User"] = orm.relationship(back_populates='reactions', uselist=False)
    reactions: Mapped[str] = mapped_column(sa.String, nullable=False)
    targets: Mapped[list["ReactionsTarget"]] = orm.relationship(back_populates="task", uselist=True, lazy="joined")

    def __repr__(self):
        return f"ReactionsTask:{self.id=}"


class ReactionsTarget(AbstractTarget):
    task: Mapped["ReactionsTask"] = orm.relationship(back_populates='targets', uselist=False)
    task_fk: Mapped[int] = mapped_column(sa.ForeignKey('reactionstask.id', ondelete='CASCADE'),
                                         unique=False, nullable=False)
    used_bots: Mapped[list["ReactionsUsedBot"]] = orm.relationship(back_populates="target", uselist=True, lazy="joined")

    def __repr__(self):
        return f"ReactionsTarget:{self.id=}"


class ReactionsUsedBot(Base):
    bot_fk: Mapped[int] = mapped_column(sa.ForeignKey('bot.id', ondelete='CASCADE'), unique=False, nullable=False)
    target_fk: Mapped[int] = mapped_column(sa.ForeignKey('reactionstarget.id', ondelete='CASCADE'),
                                           unique=False, nullable=False)
    target: Mapped["ReactionsTarget"] = orm.relationship(back_populates='used_bots', uselist=False)

    def __repr__(self):
        return f"ReactionsUsedBot:{self.id=}"
