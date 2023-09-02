from fastapi import Depends, HTTPException, status, Request, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import WebSocketException

from app.core.config import settings
from app.database import Database
from app.database.database import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/token")


async def get_db(request: Request = None) -> Database:
    if request:
        return request.state.db
    else:
        async with AsyncSession(bind=engine, expire_on_commit=False) as session:
            return Database(session)


async def authorization(token: str, db: Database, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await db.user.get_by_username(username)
    if not user:
        raise credentials_exception
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await authorization(token, db, credentials_exception)


async def get_current_user_websocket(token: str = Query(), db: Database = Depends(get_db)):
    credentials_exception = WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return await authorization(token, db, credentials_exception)
