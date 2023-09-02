from fastapi import APIRouter, Depends

from app.api import depends
from app.database import Database
from app.schemas import BotScheme, BotSchemeAdd

router = APIRouter()


@router.post("/new", response_model=BotScheme)
async def new(
    bot: BotSchemeAdd,
    db: Database = Depends(depends.get_db)
):
    bot = await db.bot.new(**bot.model_dump())
    await db.session.commit()
    return BotScheme(**bot.__dict__)
