from app.models.tasks.subscribers import SubscribersTask

from .base import TasksRepo


class SubscribersRepo(TasksRepo):
    model = SubscribersTask
