from fastapi import APIRouter

from . import subscribers, views

router = APIRouter()
router.include_router(subscribers.router)
router.include_router(views.router)
