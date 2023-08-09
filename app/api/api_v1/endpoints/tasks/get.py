from fastapi import APIRouter, Depends

from app.core import deps
from app.schemas.tasks.base import BaseSchemaAll, SchemeAllTasks
from app.schemas.users import UserSchema
from app.services.tasks.subscribers import SubscribersService
from app.services.tasks.views import ViewsService

router = APIRouter(prefix="/get")


@router.get("/all", response_model=SchemeAllTasks)
async def get_tasks(
    current_user: UserSchema = Depends(deps.get_current_user),
    views_service: ViewsService = Depends(deps.views_service),
    subscribers_service: SubscribersService = Depends(deps.subscribers_service),
):
    views_tasks = await views_service.get_tasks_user(current_user.id)
    subscribers_tasks = await subscribers_service.get_tasks_user(current_user.id)

    all_tasks = []
    in_working = []
    on_pause = []
    completed = []

    for task in views_tasks + subscribers_tasks:
        all_tasks.append(task.to_read_model())
        if task.pause:
            on_pause.append(task.to_read_model())
        if task.count > task.count_done and not task.pause:
            in_working.append(task.to_read_model())
        if task.count == task.count_done:
            completed.append(task.to_read_model())

    return SchemeAllTasks(
        all=BaseSchemaAll(count=len(all_tasks), tasks=all_tasks),
        in_working=BaseSchemaAll(count=len(in_working), tasks=in_working),
        on_pause=BaseSchemaAll(count=len(on_pause), tasks=on_pause),
        completed=BaseSchemaAll(count=len(completed), tasks=completed),
    )
