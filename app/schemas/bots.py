from pydantic import BaseModel


class BotScheme(BaseModel):
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


class BotSchemeAdd(BaseModel):
    api_id: int
    api_hash: str
    password: str
    lang_code: str
    app_version: str
    device_model: str
    session_string: str
