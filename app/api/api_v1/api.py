from fastapi import APIRouter

from app.api.api_v1.endpoints import users, tasks, bots, proxy, test_ws

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(test_ws.router, prefix="/ws", tags=["ws"])
