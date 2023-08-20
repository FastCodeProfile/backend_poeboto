from loguru import logger
from pyrogram import Client
from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered,
                             UserDeactivatedBan)

from .methods import Methods


class Telegram(Methods):
    def __init__(self, bot, proxy):
        self.bot = bot
        self.proxy = proxy

    def _get_proxy_dict(self):
        proxy_dict = dict(
            scheme=self.proxy.scheme,
            hostname=self.proxy.ip,
            port=self.proxy.port,
            username=self.proxy.username,
            password=self.proxy.password,
        )
        return proxy_dict

    async def _get_client(self):
        client = Client(
            proxy=self._get_proxy_dict(),
            name="poeboto",
            api_id=self.bot.api_id,
            api_hash=self.bot.api_hash,
            password=self.bot.password,
            lang_code=self.bot.lang_code,
            app_version=self.bot.app_version,
            device_model=self.bot.device_model,
            session_string=self.bot.session_string,
        )
        return client

    async def start(self) -> bool:
        app = await self._get_client()
        try:
            self.app = app
            await app.start()
            return True
        except (AuthKeyUnregistered, UserDeactivatedBan, AuthKeyDuplicated):
            logger.error(f"Бот №{self.bot.id} недоступен.")

    async def stop(self):
        await self.app.stop()
