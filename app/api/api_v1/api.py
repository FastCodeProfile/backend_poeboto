from fastapi import APIRouter

from app.api.api_v1.endpoints import (add_tasks, bots, chat, pause_tasks,
                                      proxies, tasks, users)

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(proxies.router, prefix="/proxies", tags=["proxies"])
api_router.include_router(add_tasks.router, prefix="/add_tasks", tags=["add_tasks"])
api_router.include_router(
    pause_tasks.router, prefix="/pause_tasks", tags=["pause_tasks"]
)
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(chat.router, prefix="/chat")
