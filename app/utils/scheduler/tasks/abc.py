from abc import ABC, abstractmethod

from app.services.use_bots import UseBotsRepo, UseBotsService

from app.utils.telegram.client import Telegram


class ABCTasks(ABC):
    use_bots_service = UseBotsService(UseBotsRepo)

    def __init__(self, client: Telegram, bot_id: int):
        self.client = client
        self.bot_id = bot_id

    @abstractmethod
    async def execution(self, this_task):
        pass
