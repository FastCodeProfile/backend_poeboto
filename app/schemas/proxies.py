from pydantic import BaseModel


class ProxyScheme(BaseModel):
    id: int
    url: str
    working: bool
    ip: str
    port: int
    scheme: str
    username: str
    password: str

    class Config:
        from_attributes = True


class ProxySchemeAdd(BaseModel):
    url: str
    ip: str
    port: int
    scheme: str
    username: str
    password: str
