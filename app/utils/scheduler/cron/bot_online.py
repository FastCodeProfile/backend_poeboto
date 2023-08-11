from loguru import logger

from app.core import deps
from app.models.proxies import Proxies
from app.utils.telegram.client import Telegram


class BotOnline:
    bots_service = deps.bots_service()
    proxies_service = deps.proxies_service()

    async def run_set_online(self, ctx):
        proxies = await self.proxies_service.get_proxies_for_working()
        if not proxies:
            logger.warning("Сейчас нет свободных прокси, задача онлайн")
            return

        await self.execution_online(proxies[0])

    async def execution_online(self, proxy: Proxies):
        logger.info(f"Выполняю задачу, онлайн ботов.")
        await self.proxies_service.proxies_repo.take(proxy.id)

        bots = await self.bots_service.get_bots_for_working()
        bots_limit = int(len(bots) * 0.2)

        for bot in bots[:bots_limit]:
            if not await self.proxies_service.rotation(proxy):
                await self.proxies_service.proxies_repo.release(proxy.id)
                return

            await self.bots_service.bots_repo.take(bot.id)

            client = Telegram(bot, proxy)
            if not await client.start():
                continue

            try:
                await client.set_online()
            except Exception as err:
                logger.error(f"Ошибка при выполнении задачи, онлайн ботов: {err}")
                await self.proxies_service.proxies_repo.release(proxy.id)
                return
            finally:
                await self.bots_service.bots_repo.release(bot.id)
                await client.stop()

        await self.proxies_service.proxies_repo.release(proxy.id)
