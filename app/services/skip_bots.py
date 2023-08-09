from app.repositories.skip_bots import SkipBotsRepository


class SkipBotsService:
    def __init__(self, skip_bots_repo: SkipBotsRepository):
        self.skip_bots_repo: SkipBotsRepository = skip_bots_repo()

    async def add_skip_bots(self, task_name, task_id: int, bot_id: int):
        data = dict(task_name=task_name, task_id=task_id, bot_id=bot_id)
        await self.skip_bots_repo.add_one(data)
