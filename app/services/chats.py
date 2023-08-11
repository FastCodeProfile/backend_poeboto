from app.repositories.chats import ChatsRepo


class ChatsService:
    def __init__(self, chats_repo: ChatsRepo):
        self.chats_repo: ChatsRepo = chats_repo()

    async def add_chat(self, task_name, task_id: int, link: str, photo: str):
        data = dict(task_name=task_name, task_id=task_id, link=link, photo=photo)
        await self.chats_repo.add_one(data)

    async def get_chats_by_task(self, task_name: str, task_id: int):
        chats = await self.chats_repo.find_chats_by_task(
            task_name, task_id
        )
        return chats

    async def get_chat_by_link(self, link):
        chat = await self.chats_repo.find_chat_by_link(link)
        return chat
