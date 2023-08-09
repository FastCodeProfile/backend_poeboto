from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int
    task: str
    link: str
    pause: bool
    avatar: str
    count: int
    count_done: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True


class BaseSchemaAll(BaseModel):
    count: int
    tasks: list[BaseSchema]


class BaseSchemaAdd(BaseModel):
    link: str
    count: int
    start_date: datetime
    end_date: datetime


class BaseSchemaModel(BaseSchema):
    done_in_hour: int
    next_start_date: datetime


class SchemeAllTasks(BaseModel):
    all: BaseSchemaAll
    in_working: BaseSchemaAll
    on_pause: BaseSchemaAll
    completed: BaseSchemaAll
