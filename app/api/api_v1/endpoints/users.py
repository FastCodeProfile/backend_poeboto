from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api import depends
from app.core.security import create_access_token, get_password_hash, verify_password
from app.database import Database
from app.schemas import SubscribersScheme, ViewsScheme, UserScheme, UserSchemeAdd, UserTokenScheme, ReactionsScheme

router = APIRouter()


@router.get("/get", response_model=UserScheme)
async def get(current_user=Depends(depends.get_current_user)):
    tasks = []

    for task in current_user.views:
        before_execution: timedelta = task.end_date - task.next_start_date
        speed = f"1 просмотр в {f'{task.delay / 60} мин' if task.delay >= 60 else f'{task.delay} сек'}"
        last_bot = task.next_start_date-timedelta(seconds=task.delay)
        tasks.append(ViewsScheme(**task.__dict__, before_execution=int(before_execution.total_seconds()),
                                 last_bot=last_bot,
                                 count=task.targets[0].count, count_done=task.targets[0].count_done,
                                 speed=speed, task_type="views"))

    for task in current_user.subscribers:
        before_execution: timedelta = task.end_date - task.next_start_date
        speed = f"1 подписчик в {f'{task.delay / 60} мин' if task.delay >= 60 else f'{task.delay} сек'}"
        last_bot = task.next_start_date-timedelta(seconds=task.delay)
        tasks.append(SubscribersScheme(**task.__dict__, before_execution=int(before_execution.total_seconds()),
                                       last_bot=last_bot,
                                       count=task.targets[0].count, count_done=task.targets[0].count_done,
                                       speed=speed, task_type="subscribers"))

    for task in current_user.reactions:
        before_execution: timedelta = task.end_date - task.next_start_date
        speed = f"1 реакция в {f'{task.delay / 60} мин' if task.delay >= 60 else f'{task.delay} сек'}"
        last_bot = task.next_start_date-timedelta(seconds=task.delay)
        tasks.append(ReactionsScheme(**task.__dict__, before_execution=int(before_execution.total_seconds()),
                                    last_bot=last_bot, count=task.targets[0].count,
                                     count_done=task.targets[0].count_done,
                                     speed=speed, task_type="reactions"))

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
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(depends.get_db)):
    user = await db.user.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username)
    return UserTokenScheme(access_token=access_token)
