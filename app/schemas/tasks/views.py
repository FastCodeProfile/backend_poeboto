from .base import BaseSchema, BaseSchemaAdd, BaseSchemaModel


class ViewsSchema(BaseSchema):
    limit: int


class ViewsSchemaAdd(BaseSchemaAdd):
    limit: int


class ViewsSchemaModel(BaseSchemaModel):
    limit: int
