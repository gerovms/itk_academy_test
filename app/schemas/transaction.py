from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class TransactionCreate(BaseModel):
    operation_type: TransactionType = Field(
        ...,
        description="Тип операции"
    )
    amount: int = Field(
        ...,
        description="Сумма"
    )
