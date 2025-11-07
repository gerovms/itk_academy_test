from pydantic import BaseModel, Field

from app.services.constants import MAX_LENGTH, MIN_LENGTH


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        description=("Имя пользователя")
    )
    password: str = Field(
        ...,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        description="Пароль пользователя",
    )
