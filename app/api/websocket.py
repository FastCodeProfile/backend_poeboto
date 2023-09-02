import asyncio

from fastapi import APIRouter, WebSocket
from fastapi.params import Depends
from websockets.exceptions import ConnectionClosedOK

from app.api import depends
from app.api.api_v1.endpoints.users import get

router = APIRouter(prefix="/ws")


@router.websocket("")
async def ws(
    websocket: WebSocket,
    current_user=Depends(depends.get_current_user_websocket)
):
    await websocket.accept()
    try:
        while True:
            result = await get(current_user)
            await websocket.send_json(result.json())
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        pass
