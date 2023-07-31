from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    login: str
    balance: float
    is_super: bool

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    login: str
    password: str


class UserTokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    class Config:
        populate_by_name = True
