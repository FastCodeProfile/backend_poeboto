from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    is_super: Mapped[bool] = mapped_column(Boolean(), default=False)
    balance: Mapped[float] = mapped_column(Float(), default=0.00)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id, login=self.login, is_super=self.is_super, balance=self.balance
        )
