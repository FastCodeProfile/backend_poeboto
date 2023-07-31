from pyrogram import Client
from pyrogram.raw.functions.account import UpdateStatus
from pyrogram.raw.functions.messages import GetMessagesViews


class Methods:
    app: Client

    async def subscribe(self, link: str):
        if not (link.startswith("https://t.me/joinchat/") or "/+" in link):
            link = f'@{link.split("https://t.me/")[1]}'
        await self.set_online()
        await self.app.join_chat(link)

    async def view(self, link: str, limit: int = 5):
        if link.startswith("https://t.me/joinchat/"):
            link = (await self.app.get_chat(link)).id
        else:
            link = f'@{link.split("https://t.me/")[1]}'
        await self.set_online()
        msg_ids = [msg.id async for msg in self.app.get_chat_history(link, limit)]
        if msg_ids:
            channel = await self.app.resolve_peer(link)
            await self.app.invoke(
                GetMessagesViews(peer=channel, id=msg_ids, increment=True)
            )

    async def set_online(self):
        await self.app.invoke(UpdateStatus(offline=False))
