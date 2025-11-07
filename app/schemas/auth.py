from pydantic import BaseModel, Field


class Token(BaseModel):

    access_token: str
    token_type: str = "bearer"


class Auth(BaseModel):

    username: str = Field(..., description="Username пользователя")
    password: str = Field(..., description="Пароль пользователя")
