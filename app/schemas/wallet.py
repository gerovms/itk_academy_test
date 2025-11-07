from pydantic import BaseModel, Field


class WalletGet(BaseModel):
    amount: int = Field(
        ...,
        description="Сумма на счету"
    )
