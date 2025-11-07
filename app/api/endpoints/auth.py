from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.user import UserCreate
from app.schemas.auth import Token, Auth
from app.crud.user import user_crud
from app.services.security import create_access_token


router = APIRouter()


@router.post("/register")
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    existing = await user_crud.get_by_username(user_in.username, session)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким username уже существует"
            )

    user = await user_crud.create_user(
        user_in.username,
        user_in.password,
        session
        )
    return {"id": user.id, "username": user.username}


@router.post("/login", response_model=Token)
async def login(
    auth_in: Auth,
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.authenticate(
        auth_in.username,
        auth_in.password,
        session
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
            )

    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}
