from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ws
from app.api.api_v1 import api
from app.core.config import settings

app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vk-service.pro"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws.router)
app.include_router(api.api_router, prefix=settings.API_V1_STR)
