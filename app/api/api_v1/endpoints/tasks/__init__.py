from fastapi import APIRouter

from . import subscribers, views, reactions

router = APIRouter()
router.include_router(subscribers.router)
router.include_router(views.router)
router.include_router(reactions.router)
