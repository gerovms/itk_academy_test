from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.transaction import TransactionType
from app.models.wallet import Wallet


class WalletCRUD(CRUDBase):
    async def get_wallet(
            self,
            id: int,
            session: AsyncSession
            ) -> Wallet | None:
        result = await session.execute(select(Wallet).where(Wallet.id == id))
        return result.scalars().first()

    async def update_balance(
            self,
            wallet: Wallet,
            operation_type: TransactionType,
            amount: int,
            session: AsyncSession
            ) -> Wallet:
        if operation_type == TransactionType.DEPOSIT:
            wallet.balance += amount
        elif operation_type == TransactionType.WITHDRAW:
            if wallet.balance < amount:
                raise ValueError("Недостаточно средств на кошельке")
            wallet.balance -= amount
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet


wallet_crud = WalletCRUD(Wallet)
