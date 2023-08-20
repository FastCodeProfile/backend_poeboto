import asyncio

from fastapi import APIRouter, Depends, WebSocket
from websockets.exceptions import ConnectionClosedOK

from app.api.api_v1.endpoints.tasks.get_everything import get_tasks
from app.api.api_v1.endpoints.users import info
from app.core import depends
from app.schemas.users import UserScheme
from app.services.tasks.subscribers import SubscribersService
from app.services.tasks.views import ViewsService

router = APIRouter()


@router.websocket("/ws/user")
async def websocket_user(
    websocket: WebSocket,
    current_user: UserScheme = Depends(depends.ws_get_current_user),
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
    current_user: UserScheme = Depends(depends.ws_get_current_user),
    views_service: ViewsService = Depends(depends.views_service),
    subscribers_service: SubscribersService = Depends(depends.subscribers_service),
):
    await websocket.accept()
    try:
        while True:
            tasks = await get_tasks(current_user, views_service, subscribers_service)
            await websocket.send_json(tasks.model_dump())
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        pass
