from app.models.tasks.views import ViewsTask

from .base import TasksRepo


class ViewsRepo(TasksRepo):
    model = ViewsTask
