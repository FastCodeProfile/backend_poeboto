from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.tasks.multiple import MultipleSchemaModel

from .base import BaseTask


class MultipleTask(BaseTask):
    __tablename__ = "multiple_task"

    task: Mapped[str] = mapped_column(String(), default="multiple_task")
    views: Mapped[bool] = mapped_column(Boolean(), default=False)
    reactions: Mapped[bool] = mapped_column(Boolean(), default=False)

    def to_read_model(self) -> MultipleSchemaModel:
        return MultipleSchemaModel(
            id=self.id,
            task=self.task,
            pause=self.pause,
            count=self.count,
            count_done=self.count_done,
            start_date=self.start_date,
            end_date=self.end_date,
            last_date_start=self.last_date_start,
            delay=self.delay,
            views=self.views,
            reactions=self.reactions
        )
