from app.repositories.bots import BotsRepo
from app.schemas.bots import BotSchemaAdd


class BotsService:
    def __init__(self, bots_repo: BotsRepo):
        self.bots_repo: BotsRepo = bots_repo()

    async def add_bot(self, bot: BotSchemaAdd):
        bot_dict = bot.model_dump()
        bot_id = await self.bots_repo.add_one(bot_dict)
        bot = await self.bots_repo.find_by_id(bot_id)
        return bot.to_read_model()

    async def get_bots(self):
        bots = await self.bots_repo.find_all()
        return bots

    async def update_bot(self, bot, last_call: bool = False):
        await self.bots_repo.update_bot(bot, last_call)

    async def get_bots_for_working(self):
        bots = await self.bots_repo.find_bots_for_working()
        return bots
