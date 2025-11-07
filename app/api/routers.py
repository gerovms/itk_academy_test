from fastapi import APIRouter

from .endpoints import auth_router, wallets_router


main_router = APIRouter()

main_router.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Аутентификация"],
)
main_router.include_router(
    wallets_router,
    prefix="/api/v1/wallets",
    tags=["Кошельки"],
)
