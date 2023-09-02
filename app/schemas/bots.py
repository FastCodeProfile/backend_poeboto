from pydantic import BaseModel


class BotScheme(BaseModel):
    id: int =1
    ban: bool = False
    api_id: int = 123
    api_hash: str = "123"
    password: str = "XxX"
    lang_code: str = "en"
    app_version: str = "1.0.0"
    device_model: str = "PC"
    session_string: str = "y767idOTr6578T^#R^"

    class Config:
        from_attributes = True


class BotSchemeAdd(BaseModel):
    api_id: int = 123
    api_hash: str = "123"
    password: str = "XxX"
    lang_code: str = "en"
    app_version: str = "1.0.0"
    device_model: str = "PC"
    session_string: str = "CYA*&O&UYKTYGYJdGKYUCUISAGFYURUASYC"
