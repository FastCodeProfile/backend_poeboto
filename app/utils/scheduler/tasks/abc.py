from abc import ABC, abstractmethod

from app.repositories.skip_bots import SkipBotsRepository
from app.services.skip_bots import SkipBotsService
from app.services.tasks import TasksService
from app.utils.telegram.client import Telegram


class ABCTasks(ABC):
    tasks_service: TasksService
    skip_bots_service = SkipBotsService(SkipBotsRepository)

    def __init__(self, client: Telegram, bot_id: int):
        self.client = client
        self.bot_id = bot_id

    @abstractmethod
    async def execution(self, this_task):
        pass
