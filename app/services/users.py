from app.repositories.users import UsersRepo
from app.schemas.users import UserSchemaAdd


class UsersService:
    def __init__(self, users_repo: UsersRepo):
        self.users_repo: UsersRepo = users_repo()

    async def add_user(self, user: UserSchemaAdd):
        if not await self.users_repo.find_by_login(user.login):
            user_dict = user.model_dump()
            user_id = await self.users_repo.add_one(user_dict)
            user = await self.users_repo.find_by_id(user_id)
            return user

    async def get_users(self):
        return await self.users_repo.find_all()

    async def update_user(self, user):
        await self.users_repo.update_user(user)

    async def get_user_by_login(self, login: str):
        return await self.users_repo.find_by_login(login)
