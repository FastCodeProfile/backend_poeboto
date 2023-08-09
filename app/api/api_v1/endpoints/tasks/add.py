from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.core import deps
from app.core.config import settings
from app.schemas.tasks.subscribers import (SubscribersSchema,
                                           SubscribersSchemaAdd)
from app.schemas.tasks.views import ViewsSchema, ViewsSchemaAdd
from app.schemas.users import UserSchema
from app.services.tasks.subscribers import SubscribersService
from app.services.tasks.views import ViewsService
from app.services.users import UsersService
from app.utils.telegram import get_avatar

router = APIRouter(prefix="/add")


@router.post("/subscribers", response_model=SubscribersSchema)
async def subscribers(
    task: SubscribersSchemaAdd,
    tasks_service: SubscribersService = Depends(deps.subscribers_service),
    users_service: UsersService = Depends(deps.users_service),
    current_user: UserSchema = Depends(deps.get_current_user),
):
    avatar = await get_avatar(task.link)
    price = task.count * settings.PRICE
    task.start_date = task.start_date.replace(tzinfo=None)
    task.end_date = task.end_date.replace(tzinfo=None)
    if current_user.balance >= price:
        current_user.balance -= price
        await users_service.update_user(current_user)
        created_task = await tasks_service.add_task(task, current_user.id, avatar)
        logger.info(f"Создана новая задача, накрутка подписчиков. - {created_task}")
        return created_task
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")


@router.post("/views", response_model=ViewsSchema)
async def views(
    task: ViewsSchemaAdd,
    tasks_service: ViewsService = Depends(deps.views_service),
    users_service: UsersService = Depends(deps.users_service),
    current_user: UserSchema = Depends(deps.get_current_user),
):
    if "/+" in task.link:
        raise HTTPException(
            status_code=404, detail="Ссылка на канал должна быть публичной."
        )

    avatar = await get_avatar(task.link)
    task.start_date = task.start_date.replace(tzinfo=None)
    task.end_date = task.end_date.replace(tzinfo=None)
    price = task.count * settings.PRICE
    if current_user.balance >= price:
        current_user.balance -= price
        await users_service.update_user(current_user)
        created_task = await tasks_service.add_task(task, current_user.id, avatar)
        logger.info(f"Создана новая задача, накрутка просмотров. - {created_task}")
        return created_task
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")