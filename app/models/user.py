from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mp

from app.core.db import Base
from app.models.wallet import Wallet
from app.services.constants import MAX_LENGTH


class User(Base):

    __tablename__ = "users"

    username: Mapped[str] = mp(
        String(MAX_LENGTH),
        nullable=False
        )
    password: Mapped[str] = mp(
        String(MAX_LENGTH),
        nullable=False
        )
    wallet: Mapped["Wallet"] = relationship(
        "Wallet",
        back_populates="user",
        lazy="selectin",
    )
