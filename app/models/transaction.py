from enum import Enum

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mp

from app.core.db import Base


class TransactionType(str, Enum):

    __tablename__ = "transactions_types"

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Transaction(Base):

    __tablename__ = "transactions"

    operation_type: Mapped[TransactionType] = mp(
        ENUM(
            TransactionType,
            name="operation_type_enum",
            nullable=False,
        )
    )
    amount: Mapped[int] = mp(
        Integer,
        nullable=False
    )
