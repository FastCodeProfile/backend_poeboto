from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models import User, ViewsTask, SubscribersTask


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        username: str | None = None,
        password: str | None = None,
        views: list["ViewsTask"] = [],
        subscribers: list["SubscribersTask"] = []
    ) -> User:
        new_user = await self.session.merge(
            User(
                username=username,
                password=password,
                views=views,
                subscribers=subscribers
            )
        )
        return new_user

    async def get_by_username(self, username: str) -> User:
        user = await self.get_by_where(User.username == username)
        return user
