from .base import BaseSchema, BaseSchemaAdd, BaseSchemaModel


class SubscribersSchema(BaseSchema):
    link: str
    photo: str


class SubscribersSchemaAdd(BaseSchemaAdd):
    link: str


class SubscribersSchemaModel(BaseSchemaModel):
    pass
