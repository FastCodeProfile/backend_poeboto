from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette.exceptions import WebSocketException

from app.core.config import settings
from app.repositories.bots import BotsRepository
from app.repositories.proxies import ProxiesRepository
from app.repositories.tasks.subscribers import SubscribersRepo
from app.repositories.tasks.views import ViewsRepo
from app.repositories.users import UsersRepository
from app.services.bots import BotsService
from app.services.proxies import ProxiesService
from app.services.tasks.subscribers import SubscribersService
from app.services.tasks.views import ViewsService
from app.services.users import UsersService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/token")


def bots_service():
    return BotsService(BotsRepository)


def proxies_service():
    return ProxiesService(ProxiesRepository)


def users_service():
    return UsersService(UsersRepository)


def subscribers_service():
    return SubscribersService(SubscribersRepo)


def views_service():
    return ViewsService(ViewsRepo)


async def authorization(
    token: str, users_service_: UsersService, credentials_exception
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        login: str = payload.get("login")
        if not login:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await users_service_.get_user_by_login(login)
    if not user:
        raise credentials_exception

    return user.to_read_model()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users_service_: Annotated[UsersService, Depends(users_service)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await authorization(token, users_service_, credentials_exception)


async def ws_get_current_user(
    token: Annotated[str | None, Query()],
    users_service_: Annotated[UsersService, Depends(users_service)],
):
    credentials_exception = WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return await authorization(token, users_service_, credentials_exception)
