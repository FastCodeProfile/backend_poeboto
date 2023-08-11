from .base import BaseSchema, BaseSchemaAdd, BaseSchemaModel


class MultipleSchema(BaseSchema):
    links: list[str]
    photos: list[str]
    views: bool
    reactions: bool


class MultipleSchemaAdd(BaseSchemaAdd):
    links: list[str]
    views: bool
    reactions: bool


class MultipleSchemaModel(BaseSchemaModel):
    views: bool
    reactions: bool
