from app.models.tasks.multiple import MultipleTask

from .base import TasksRepo


class MultipleRepo(TasksRepo):
    model = MultipleTask
