from pydantic import BaseModel


class ProxyScheme(BaseModel):
    id: int = 1
    url: str = "https://..."
    working: bool = True
    ip: str = "127.0.0.1"
    port: int = 5050
    scheme: str = "socks5"
    username: str = "user"
    password: str = "pass"

    class Config:
        from_attributes = True


class ProxySchemeAdd(BaseModel):
    url: str = "https://..."
    ip: str = "127.0.0.1"
    port: int = 5050
    scheme: str = "socks5"
    username: str = "user"
    password: str = "pass"
