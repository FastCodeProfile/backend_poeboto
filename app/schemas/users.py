from pydantic import BaseModel


class UserScheme(BaseModel):
    id: int = 0
    balance: float = 0.00
    username: str = "username"
    tasks: list

    class Config:
        from_attributes = True


class UserSchemeAdd(BaseModel):
    username: str = "username"
    password: str = "password"


class UserTokenScheme(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    class Config:
        populate_by_name = True
