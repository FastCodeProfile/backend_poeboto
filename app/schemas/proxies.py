from pydantic import BaseModel


class ProxySchema(BaseModel):
    id: int
    work: bool
    scheme: str
    rotation_url: str
    ip: str
    port: int
    username: str
    password: str

    class Config:
        from_attributes = True


class ProxySchemaAdd(BaseModel):
    scheme: str
    rotation_url: str
    ip: str
    port: int
    username: str
    password: str
