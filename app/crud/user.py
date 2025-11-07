from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.user import User
from app.models.wallet import Wallet
from app.services.security import get_password_hash, verify_password


class UserCRUD(CRUDBase):


    async def get_by_username(self,
                              username: str,
                              session: AsyncSession) -> Optional[User]:

        result = await session.execute(select(User).where(
            User.username == username
            ))
        return result.scalars().first()

    async def create_user(
            self,
            username: str,
            password: str,
            session: AsyncSession
            ) -> User:

        hashed_password = get_password_hash(password)
        user = User(username=username, password=hashed_password)
        wallet = Wallet(balance=0, user=user)
        user.wallet = wallet
        session.add(user)
        await session.commit()
        await session.refresh(user)
        await session.refresh(wallet)
        return user

    async def authenticate(
            self,
            username: str,
            password: str,
            session: AsyncSession
            ) -> Optional[User]:

        user = await self.get_by_username(username, session)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user_crud = UserCRUD(User)
