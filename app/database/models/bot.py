from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Bot(Base):
    ban: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    busy: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    last_call = mapped_column(sa.DateTime, default=datetime.now())
    api_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    api_hash: Mapped[str] = mapped_column(sa.String, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    lang_code: Mapped[str] = mapped_column(sa.String, nullable=False)
    app_version: Mapped[str] = mapped_column(sa.String, nullable=False)
    device_model: Mapped[str] = mapped_column(sa.String, nullable=False)
    session_string: Mapped[str] = mapped_column(sa.Text, nullable=False)

    def __repr__(self):
        return f"Bot:{self.id=}"
