from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.tasks.views import ViewsSchemaModel

from .base import BaseTask


class ViewsTask(BaseTask):
    __tablename__ = "views_task"

    task: Mapped[str] = mapped_column(String(), default="views")
    limit: Mapped[int] = mapped_column(Integer(), default=0)

    def to_read_model(self) -> ViewsSchemaModel:
        return ViewsSchemaModel(
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
            limit=self.limit,
        )
