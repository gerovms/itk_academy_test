from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mp

from app.core.db import Base


class Wallet(Base):

    __tablename__ = "wallets"

    balance: Mapped[int] = mp(
        Integer,
        default=0
    )
    user_id: Mapped[int] = mp(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="wallet")
