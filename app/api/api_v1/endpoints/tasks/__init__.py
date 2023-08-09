from fastapi import APIRouter

from . import add, get, pause

router = APIRouter()
router.include_router(add.router)
router.include_router(get.router)
router.include_router(pause.router)
