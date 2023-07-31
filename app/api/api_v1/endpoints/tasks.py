from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.tasks import TaskSchemaAll, TaskSchemeAllStates
from app.schemas.users import UserSchema
from app.services.tasks import TasksService

router = APIRouter()


@router.get("/get_tasks", response_model=TaskSchemeAllStates)
async def get_tasks(
    current_user: UserSchema = Depends(deps.get_current_user),
    views_service: TasksService = Depends(deps.views_tasks_service),
    subscribers_service: TasksService = Depends(deps.subscribers_tasks_service),
):
    all_views_tasks = await views_service.get_tasks_user(current_user.id)
    all_subscribers_tasks = await subscribers_service.get_tasks_user(current_user.id)
    all_tasks = all_views_tasks + all_subscribers_tasks
    all_count = len(all_tasks)
    all_tasks_read_model = [task.to_read_model() for task in all_tasks]
    all_tasks_scheme = TaskSchemaAll(count=all_count, tasks=all_tasks_read_model)
    pending_tasks_scheme = await get_tasks_pending(
        current_user, views_service, subscribers_service
    )
    in_progress_tasks_scheme = await get_tasks_in_progress(
        current_user, views_service, subscribers_service
    )
    completed_tasks_scheme = await get_tasks_completed(
        current_user, views_service, subscribers_service
    )
    return TaskSchemeAllStates(
        all=all_tasks_scheme,
        pending=pending_tasks_scheme,
        in_progress=in_progress_tasks_scheme,
        completed=completed_tasks_scheme,
    )


@router.get("/get_tasks_pending", response_model=TaskSchemaAll)
async def get_tasks_pending(
    current_user: UserSchema = Depends(deps.get_current_user),
    views_service: TasksService = Depends(deps.views_tasks_service),
    subscribers_service: TasksService = Depends(deps.subscribers_tasks_service),
):
    views_tasks = await views_service.get_tasks_user_pending(current_user.id)
    subscribers_tasks = await subscribers_service.get_tasks_user_pending(
        current_user.id
    )
    tasks = views_tasks + subscribers_tasks
    count = len(tasks)
    tasks_read_model = [task.to_read_model() for task in tasks]
    return TaskSchemaAll(count=count, tasks=tasks_read_model)


@router.get("/get_tasks_in_progress", response_model=TaskSchemaAll)
async def get_tasks_in_progress(
    current_user: UserSchema = Depends(deps.get_current_user),
    views_service: TasksService = Depends(deps.views_tasks_service),
    subscribers_service: TasksService = Depends(deps.subscribers_tasks_service),
):
    views_tasks = await views_service.get_tasks_user_in_progress(current_user.id)
    subscribers_tasks = await subscribers_service.get_tasks_user_in_progress(
        current_user.id
    )
    tasks = views_tasks + subscribers_tasks
    count = len(tasks)
    tasks_read_model = [task.to_read_model() for task in tasks]
    return TaskSchemaAll(count=count, tasks=tasks_read_model)


@router.get("/get_tasks_completed", response_model=TaskSchemaAll)
async def get_tasks_completed(
    current_user: UserSchema = Depends(deps.get_current_user),
    views_service: TasksService = Depends(deps.views_tasks_service),
    subscribers_service: TasksService = Depends(deps.subscribers_tasks_service),
):
    views_tasks = await views_service.get_tasks_user_completed(current_user.id)
    subscribers_tasks = await subscribers_service.get_tasks_user_completed(
        current_user.id
    )
    tasks = views_tasks + subscribers_tasks
    count = len(tasks)
    tasks_read_model = [task.to_read_model() for task in tasks]
    return TaskSchemaAll(count=count, tasks=tasks_read_model)
