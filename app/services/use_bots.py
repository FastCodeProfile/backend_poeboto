from app.repositories.use_bots import UseBotsRepo


class UseBotsService:
    def __init__(self, use_bots_repo: UseBotsRepo):
        self.use_bots_repo: UseBotsRepo = use_bots_repo()

    async def add_use_bot(self, chat_id: int, bot_id: int):
        data = dict(chat_id=chat_id, bot_id=bot_id)
        await self.use_bots_repo.add_one(data)

    async def existing(self, chat_id: int, bot_id: int):
        return await self.use_bots_repo.find_existing(chat_id, bot_id)

