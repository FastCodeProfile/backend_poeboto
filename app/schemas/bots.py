from pydantic import BaseModel


class BotSchema(BaseModel):
    id: int
    ban: bool
    api_id: int
    api_hash: str
    password: str
    lang_code: str
    app_version: str
    device_model: str
    session_string: str

    class Config:
        from_attributes = True


class BotSchemaAdd(BaseModel):
    api_id: int
    api_hash: str
    password: str
    lang_code: str
    app_version: str
    device_model: str
    session_string: str


class BotSchemaAll(BaseModel):
    count: int
    bots: list[BotSchema]
