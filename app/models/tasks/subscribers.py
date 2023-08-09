from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.tasks.subscribers import SubscribersSchemaModel

from .base import BaseTask


class SubscribersTask(BaseTask):
    __tablename__ = "subscribers_task"

    task: Mapped[str] = mapped_column(String(), default="subscribers")

    def to_read_model(self) -> SubscribersSchemaModel:
        return SubscribersSchemaModel(
            id=self.id,
            task=self.task,
            link=self.link,
            pause=self.pause,
            avatar=self.avatar,
            count=self.count,
            count_done=self.count_done,
            start_date=self.start_date,
            end_date=self.end_date,
            done_in_hour=self.done_in_hour,
            next_start_date=self.next_start_date,
        )
