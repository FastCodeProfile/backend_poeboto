from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.schemas.proxies import ProxySchema


class Proxies(Base):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(primary_key=True)
    work: Mapped[bool] = mapped_column(Boolean(), default=True)
    scheme: Mapped[str] = mapped_column(String(), default="http")
    rotation_url: Mapped[str] = mapped_column(String(), nullable=False)
    ip: Mapped[str] = mapped_column(String(), nullable=False)
    busy: Mapped[bool] = mapped_column(Boolean(), default=False)
    port: Mapped[int] = mapped_column(Integer(), nullable=False)
    username: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)

    def to_read_model(self) -> ProxySchema:
        return ProxySchema(
            id=self.id,
            work=self.work,
            scheme=self.scheme,
            rotation_url=self.rotation_url,
            ip=self.ip,
            port=self.port,
            username=self.username,
            password=self.password,
        )
