from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    name: str
    link: str
    url_avatar: str
    count: int
    pause: bool
    completed: bool
    in_progress: bool
    count_done: int

    class Config:
        from_attributes = True


class ViewsSchema(TaskSchema):
    limit: int


class TaskSchemaAdd(BaseModel):
    count: int
    link: str


class ViewsSchemaAdd(TaskSchemaAdd):
    limit: int


class TaskSchemaAll(BaseModel):
    count: int
    tasks: list[TaskSchema]


class TaskSchemeAllStates(BaseModel):
    all: TaskSchemaAll
    pending: TaskSchemaAll
    in_progress: TaskSchemaAll
    completed: TaskSchemaAll
