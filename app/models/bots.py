from datetime import datetime as dt

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.schemas.bots import BotSchema


class Bots(Base):
    __tablename__ = "bots"

    id: Mapped[int] = mapped_column(primary_key=True)
    ban: Mapped[bool] = mapped_column(Boolean(), default=False)
    busy: Mapped[bool] = mapped_column(Boolean(), default=False)
    api_id: Mapped[str] = mapped_column(Integer(), nullable=False)
    api_hash: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    lang_code: Mapped[str] = mapped_column(String(), nullable=False)
    app_version: Mapped[str] = mapped_column(String(), nullable=False)
    device_model: Mapped[str] = mapped_column(String(), nullable=False)
    session_string: Mapped[str] = mapped_column(String(), nullable=False)
    last_call = mapped_column(DateTime(), default=dt.now())

    def to_read_model(self) -> BotSchema:
        return BotSchema(
            id=self.id,
            ban=self.ban,
            api_id=self.api_id,
            api_hash=self.api_hash,
            password=self.password,
            lang_code=self.lang_code,
            app_version=self.app_version,
            device_model=self.device_model,
            session_string=self.session_string,
        )
