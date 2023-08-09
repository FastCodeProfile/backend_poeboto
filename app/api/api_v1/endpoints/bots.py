from fastapi import APIRouter, Depends

from app.core import deps
from app.schemas.bots import BotSchema, BotSchemaAdd
from app.services.bots import BotsService

router = APIRouter()


@router.post("/add_bot", response_model=BotSchema)
async def add_bot(
    bot: BotSchemaAdd,
    bots_service: BotsService = Depends(deps.bots_service),
):
    return await bots_service.add_bot(bot)
