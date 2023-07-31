import asyncio

from fastapi import APIRouter, Depends, WebSocket
from websockets.exceptions import ConnectionClosedOK

from app.api import deps
from app.api.api_v1.endpoints.tasks import get_tasks
from app.api.api_v1.endpoints.users import info
from app.schemas.users import UserSchema
from app.services.tasks import TasksService

router = APIRouter()


@router.websocket("/ws/user")
async def websocket_user(
    websocket: WebSocket,
    current_user: UserSchema = Depends(deps.ws_get_current_user),
):
    await websocket.accept()
    try:
        while True:
            user_info = await info(current_user)
            await websocket.send_json(user_info.model_dump())
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        pass


@router.websocket("/ws/get_tasks")
async def websocket_get_tasks(
    websocket: WebSocket,
    current_user: UserSchema = Depends(deps.ws_get_current_user),
    views_service: TasksService = Depends(deps.views_tasks_service),
    subscribers_service: TasksService = Depends(deps.subscribers_tasks_service),
):
    await websocket.accept()
    try:
        while True:
            tasks = await get_tasks(current_user, views_service, subscribers_service)
            await websocket.send_json(tasks.model_dump())
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        pass
