from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from app.core.config import settings
from .repositories import (ViewsTaskRepo, UserRepo, SubscribersTaskRepo, ProxyRepo, BotRepo, ViewsTargetRepo,
                           SubscribersTargetRepo, SubscribersUsedBotRepo, ViewsUsedBotRepo)


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=False, pool_pre_ping=True)


engine = create_async_engine(settings.pg_dns)


class Database:
    bot: BotRepo
    user: UserRepo
    proxy: ProxyRepo

    views_task: ViewsTaskRepo
    views_used_bot: ViewsUsedBotRepo
    views_target: ViewsTargetRepo

    subscribers_task: SubscribersTaskRepo
    subscribers_used_bot: SubscribersUsedBotRepo
    subscribers_target: SubscribersTargetRepo

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        bot: BotRepo = None,
        user: UserRepo = None,
        proxy: ProxyRepo = None,

        views_task: ViewsTaskRepo = None,
        views_used_bot: ViewsUsedBotRepo = None,
        views_target: ViewsTargetRepo = None,

        subscribers_task: SubscribersTaskRepo = None,
        subscribers_used_bot: SubscribersUsedBotRepo = None,
        subscribers_target: SubscribersTargetRepo = None,
    ):
        self.session = session
        self.bot = bot or BotRepo(session=session)
        self.user = user or UserRepo(session=session)
        self.proxy = proxy or ProxyRepo(session=session)

        self.views_task = views_task or ViewsTaskRepo(session=session)
        self.views_used_bot = views_used_bot or ViewsUsedBotRepo(session=session)
        self.views_target = views_target or ViewsTargetRepo(session=session)

        self.subscribers_task = subscribers_task or SubscribersTaskRepo(session=session)
        self.subscribers_used_bot = subscribers_used_bot or SubscribersUsedBotRepo(session=session)
        self.subscribers_target = subscribers_target or SubscribersTargetRepo(session=session)
