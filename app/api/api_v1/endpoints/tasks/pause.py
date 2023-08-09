from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.core import deps
from app.schemas.tasks.subscribers import SubscribersSchema
from app.schemas.tasks.views import ViewsSchema
from app.schemas.users import UserSchema
from app.services.tasks.subscribers import SubscribersService
from app.services.tasks.views import ViewsService

router = APIRouter(prefix="/pause")


@router.post("/subscribers", response_model=SubscribersSchema)
async def subscribers(
    task_id: int,
    tasks_service: SubscribersService = Depends(deps.subscribers_service),
    current_user: UserSchema = Depends(deps.get_current_user),
):
    task = await tasks_service.tasks_repo.find_task_by_id(task_id)
    if task:
        if task.user_id == current_user.id:
            task = task.to_read_model()
            if task.pause:
                task.pause = False
            else:
                task.pause = True
            await tasks_service.update_task(task)
            logger.info(
                f"Задача №{task.id}, {'поставлена на паузу' if task.pause else 'снята с паузы'}."
            )
            return task
        else:
            raise HTTPException(status_code=404, detail="Вы не создатель задачи.")
    else:
        raise HTTPException(status_code=404, detail="Такой задачи не существует.")


@router.post("/views", response_model=ViewsSchema)
async def views(
    task_id: int,
    tasks_service: ViewsService = Depends(deps.views_service),
    current_user: UserSchema = Depends(deps.get_current_user),
):
    task = await tasks_service.tasks_repo.find_task_by_id(task_id)
    if task:
        if task.user_id == current_user.id:
            task = task.to_read_model()
            if task.pause:
                task.pause = False
            else:
                task.pause = True
            await tasks_service.update_task(task)
            logger.info(
                f"Задача №{task.id}, {'поставлена на паузу' if task.pause else 'снята с паузы'}."
            )
            return task
        else:
            raise HTTPException(status_code=404, detail="Вы не создатель задачи.")
    else:
        raise HTTPException(status_code=404, detail="Такой задачи не существует.")
