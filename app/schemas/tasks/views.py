from .base import BaseSchema, BaseSchemaAdd, BaseSchemaModel


class ViewsSchema(BaseSchema):
    limit: int
    link: str
    photo: str


class ViewsSchemaAdd(BaseSchemaAdd):
    limit: int
    link: str


class ViewsSchemaModel(BaseSchemaModel):
    limit: int
