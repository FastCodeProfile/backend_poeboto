from fastapi import APIRouter, Depends

from app.api import depends
from app.database import Database
from app.schemas import ProxyScheme, ProxySchemeAdd

router = APIRouter()


@router.post("/new", response_model=ProxyScheme)
async def new(
    proxy: ProxySchemeAdd,
    db: Database = Depends(depends.get_db)
):
    proxy = await db.proxy.new(**proxy.model_dump())
    await db.session.commit()
    return ProxyScheme(**proxy.__dict__)
