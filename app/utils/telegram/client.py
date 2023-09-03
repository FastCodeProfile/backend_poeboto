from asyncio import CancelledError

from loguru import logger
from pyrogram import Client
from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered,
                             UserDeactivatedBan)

from .methods import Methods
from ...database import Database
from ...database.models import Bot, Proxy


class TgClient(Methods):
    bot_id: int
    proxy_id: int

    def __init__(self, bot_generator, db: Database):
        self.db = db
        self.bots = bot_generator

    async def _get_bot(self) -> Bot:
        bot = next(self.bots)
        self.bot_id = bot.id
        return bot

    @staticmethod
    def _get_proxy_dict(proxy: Proxy) -> dict:
        proxy_dict = dict(
            scheme=proxy.scheme,
            hostname=proxy.ip,
            port=proxy.port,
            username=proxy.username,
            password=proxy.password,
        )
        return proxy_dict

    async def _get_client(self, bot: Bot, proxy: Proxy) -> Client:
        proxy_dict = self._get_proxy_dict(proxy)
        client = Client(
            name=bot.id,
            proxy=proxy_dict,
            api_id=bot.api_id,
            api_hash=bot.api_hash,
            password=bot.password,
            lang_code=bot.lang_code,
            app_version=bot.app_version,
            device_model=bot.device_model,
            session_string=bot.session_string,
        )
        return client

    async def start(self, proxy: Proxy) -> bool:
        self.proxy_id = proxy.id
        try:
            bot = await self._get_bot()
            await self.db.bot.update(bot.id, busy=True)
            await self.db.session.commit()
        except Exception as e:
            await self.db.proxy.update(proxy.id, busy=False)
            await self.db.session.commit()
            logger.error("Боты закончились!")
            return False
        client = await self._get_client(bot, proxy)
        try:
            await client.start()
            self.app = client
            logger.success(f"Бот №{bot.id} готов к работе!")
            return True
        except (AuthKeyUnregistered, UserDeactivatedBan, AuthKeyDuplicated, CancelledError):
            logger.error(f"Бот №{bot.id} недоступен. Меняю бота!")
            await self.db.bot.update(bot.id, busy=False, ban=True)
            await self.db.session.commit()
            return await self.start(proxy)

    async def stop(self):
        await self.app.stop()
