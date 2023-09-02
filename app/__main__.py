from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import websocket
from app.api.api_v1 import api
from app.core.config import settings
from app.database import Database
from app.database.database import engine

app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json")


@app.middleware("http")
async def session_db(request: Request, call_next):
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        request.state.db = Database(session)
        response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["https://vk-service.pro"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket.router)
app.include_router(api.api_router, prefix=settings.API_V1_STR)
