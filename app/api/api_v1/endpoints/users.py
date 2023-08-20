from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.core import depends
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db import Database
from app.schemas import SubscribersScheme, ViewsScheme, UserScheme, UserSchemeAdd, UserTokenScheme

router = APIRouter()


@router.get("/get", response_model=UserScheme)
async def get(current_user=Depends(depends.get_current_user)):
    tasks = []

    for task in current_user.views:
        tasks.append(ViewsScheme(**task.__dict__, task_type="views"))

    for task in current_user.subscribers:
        tasks.append(SubscribersScheme(**task.__dict__, task_type="subscribers"))

    return UserScheme(**current_user.__dict__, tasks=tasks)


@router.post("/new", response_model=UserTokenScheme)
async def new(user: UserSchemeAdd, db: Database = Depends(depends.get_db)):
    user_exists = await db.user.get_by_username(user.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Такой пользователь уже зарегистрирован.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hash_password = get_password_hash(user.password)
    await db.user.new(user.username, hash_password)
    await db.session.commit()
    access_token = create_access_token(user.username)
    return UserTokenScheme(access_token=access_token)


@router.post("/token", response_model=UserTokenScheme)
async def token(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Database = Depends(depends.get_db)):
    user = await db.user.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username)
    return UserTokenScheme(access_token=access_token)
