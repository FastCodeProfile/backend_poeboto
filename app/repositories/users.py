from app.models.users import Users
from app.utils.repository import SQLAlchemyRepository


class UsersRepo(SQLAlchemyRepository):
    model = Users

    async def update_user(self, user):
        await self.update(user.model_dump(), self.model.id == user.id)

    async def find_by_id(self, user_id: int):
        return await self.find_one(self.model.id == user_id)

    async def find_by_login(self, login: str):
        return await self.find_one(self.model.login == login)
