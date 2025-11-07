from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.transaction import TransactionCreate
from app.schemas.wallet import WalletGet
from app.crud.wallet import wallet_crud
from app.models.transaction import TransactionType
from app.models.user import User
from app.services.security import get_current_user


router = APIRouter()


@router.post(
    "/{wallet_id}/operation",
    response_model=WalletGet,
)
async def wallet_transaction(
    wallet_id: int,
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> WalletGet:
    transaction_type = TransactionType(transaction.operation_type)
    transaction_amount = transaction.amount
    user_wallet = await wallet_crud.get_wallet(
        wallet_id,
        session
        )
    if not user_wallet:
        raise HTTPException(
            status_code=404,
            detail="Кошелёк не найден"
            )
    if user_wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете управлять чужим кошельком"
        )
    return WalletGet(amount=(await wallet_crud.update_balance(
        user_wallet,
        transaction_type,
        transaction_amount,
        session
    )).balance)


@router.get(
    "/{wallet_id}",
    response_model=WalletGet
)
async def get_wallet_info(
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_wallet = await wallet_crud.get_wallet(wallet_id, session)
    if not user_wallet:
        raise HTTPException(
            status_code=404,
            detail="Кошелёк не найден"
            )
    if user_wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете иметь доступ к чужому кошельку"
        )
    return WalletGet(amount=user_wallet.balance)
