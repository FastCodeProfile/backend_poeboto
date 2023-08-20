import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Proxy(Base):
    url: Mapped[str] = mapped_column(sa.String, nullable=False)
    busy: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    working: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    ip: Mapped[str] = mapped_column(sa.String, nullable=False)
    port: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    scheme: Mapped[str] = mapped_column(sa.String, default="socks5")
    username: Mapped[str] = mapped_column(sa.String, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)

    def __repr__(self):
        return f"Proxy:{self.id=}"
