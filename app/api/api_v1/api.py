from fastapi import APIRouter

from app.api.api_v1.endpoints import bots, chat, proxies, tasks, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(proxies.router, prefix="/proxies", tags=["proxies"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(chat.router, prefix="/chat")
