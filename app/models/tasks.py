from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.schemas.tasks import TaskSchema, ViewsSchema


class BaseTasks(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(), nullable=False)
    url_avatar: Mapped[str] = mapped_column(String(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pause: Mapped[bool] = mapped_column(Boolean(), default=False)
    completed: Mapped[bool] = mapped_column(Boolean(), default=False)
    in_progress: Mapped[bool] = mapped_column(Boolean(), default=False)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    count_done: Mapped[int] = mapped_column(Integer(), default=0)
    skip_bots: Mapped[int] = mapped_column(Integer(), default=0)


class SubscribersTasks(BaseTasks):
    __tablename__ = "subscribers_tasks"

    name: Mapped[str] = mapped_column(String(), default="subscribers")

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            name=self.name,
            link=self.link,
            url_avatar=self.url_avatar,
            count=self.count,
            pause=self.pause,
            completed=self.completed,
            in_progress=self.in_progress,
            count_done=self.count_done,
        )


class ViewsTasks(BaseTasks):
    __tablename__ = "views_tasks"

    name: Mapped[str] = mapped_column(String(), default="views")
    limit: Mapped[int] = mapped_column(Integer(), default=0)

    def to_read_model(self) -> ViewsSchema:
        return ViewsSchema(
            id=self.id,
            name=self.name,
            link=self.link,
            url_avatar=self.url_avatar,
            count=self.count,
            pause=self.pause,
            completed=self.completed,
            in_progress=self.in_progress,
            count_done=self.count_done,
            limit=self.limit,
        )
