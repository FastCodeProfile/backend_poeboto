from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.api import deps
from app.core.config import settings
from app.schemas.tasks import (TaskSchema, TaskSchemaAdd, ViewsSchema,
                               ViewsSchemaAdd)
from app.schemas.users import UserSchema
from app.services.tasks import TasksService
from app.services.users import UsersService
from app.utils.telegram import get_avatar

router = APIRouter()


@router.post("/subscribers", response_model=TaskSchema)
async def subscribers(
    task: TaskSchemaAdd,
    tasks_service: TasksService = Depends(deps.subscribers_tasks_service),
    users_service: UsersService = Depends(deps.users_service),
    current_user: UserSchema = Depends(deps.get_current_user),
):
    url_avatar = await get_avatar(task.link)
    price = task.count * settings.PRICE
    if current_user.balance >= price:
        current_user.balance -= price
        await users_service.update_user(current_user)
        created_task = await tasks_service.add_task(task, current_user.id, url_avatar)
        logger.info(f"Создана новая задача, накрутка подписчиков. - {created_task}")
        return created_task
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")


@router.post("/views", response_model=ViewsSchema)
async def views(
    task: ViewsSchemaAdd,
    tasks_service: TasksService = Depends(deps.views_tasks_service),
    users_service: UsersService = Depends(deps.users_service),
    current_user: UserSchema = Depends(deps.get_current_user),
):
    if "/+" in task.link:
        raise HTTPException(status_code=404, detail="Ссылка на канал должна быть публичной.")

    url_avatar = await get_avatar(task.link)
    price = task.count * settings.PRICE
    if current_user.balance >= price:
        current_user.balance -= price
        await users_service.update_user(current_user)
        created_task = await tasks_service.add_task(task, current_user.id, url_avatar)
        logger.info(f"Создана новая задача, накрутка просмотров. - {created_task}")
        return created_task
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")


# @router.post("/reactions", response_model=TaskSchema)
# async def reactions(
#     task: TaskSchemaAdd,
#     tasks_service: TasksService = Depends(deps.tasks_service),
#     users_service: UsersService = Depends(deps.users_service),
#     current_user: UserSchema = Depends(deps.get_current_user),
# ):
#     price = task.count * settings.PRICE
#     task.reactions = ",".join(task.reactions)
#     if current_user.balance >= price:
#         current_user.balance -= price
#         await users_service.update_user(current_user)
#         created_task = await tasks_service.add_task(task, "Реакции", current_user.id)
#         logger.info(f"Создана новая задача, накрутка реакций. - {created_task}")
#         return created_task
#     else:
#         raise HTTPException(status_code=404, detail="У вас не достаточно средств.")
#
#
# @router.post("/comments", response_model=TaskSchema)
# async def comments(
#     task: CommentsSchemaAdd,
#     tasks_service: TasksService = Depends(deps.tasks_service),
#     users_service: UsersService = Depends(deps.users_service),
#     current_user: UserSchema = Depends(deps.get_current_user),
# ):
#     price = task.count * settings.PRICE
#     task.comments = ",".join(task.comments)
#     if current_user.balance >= price:
#         current_user.balance -= price
#         await users_service.update_user(current_user)
#         created_task = await tasks_service.add_task(
#             task, "Комментарии", current_user.id
#         )
#         logger.info(f"Создана новая задача, накрутка комментариев. - {created_task}")
#         return created_task
#     else:
#         raise HTTPException(status_code=404, detail="У вас не достаточно средств.")
#
#
# @router.post("/voting", response_model=TaskSchema)
# async def voting(
#     task: TaskSchemaAdd,
#     tasks_service: TasksService = Depends(deps.tasks_service),
#     users_service: UsersService = Depends(deps.users_service),
#     current_user: UserSchema = Depends(deps.get_current_user),
# ):
#     price = task.count * settings.PRICE
#     if current_user.balance >= price:
#         current_user.balance -= price
#         await users_service.update_user(current_user)
#         created_task = await tasks_service.add_task(
#             task, "Голосования", current_user.id
#         )
#         logger.info(f"Создана новая задача, накрутка голосований. - {created_task}")
#         return created_task
#     else:
#         raise HTTPException(status_code=404, detail="У вас не достаточно средств.")
