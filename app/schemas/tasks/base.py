from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int
    task: str
    pause: bool
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
    count: int
    start_date: datetime
    end_date: datetime


class BaseSchemaModel(BaseSchema):
    last_date_start: datetime
    delay: int


class SchemeAllTasks(BaseModel):
    all: BaseSchemaAll
    in_working: BaseSchemaAll
    on_pause: BaseSchemaAll
    completed: BaseSchemaAll
