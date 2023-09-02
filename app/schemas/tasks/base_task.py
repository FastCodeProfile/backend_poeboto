from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TargetScheme(BaseModel):
    photo: str = "Отсутствует"
    target: str = "https://t.me/poeboto"
    count: int = 1
    count_done: int = 0
    error: str | None = "Ошибка..."

    class Config:
        from_attributes = True


class BaseScheme(BaseModel):
    id: int = 0
    task_type: str = "views"
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()
    pause: bool = False
    completed: bool = False
    before_execution: datetime
    speed: str
    count: int
    count_done: int
    last_bot: datetime
    targets: list[TargetScheme]

    class Config:
        from_attributes = True


class BaseSchemeAdd(BaseModel):
    count: int = 1
    targets: list[str] = ["https://t.me/poeboto"]
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()
