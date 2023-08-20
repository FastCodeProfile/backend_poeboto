from fastapi import APIRouter

from app.api.api_v1.endpoints import users, tasks, bots, proxy

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
