from pydantic_settings import BaseSettings, SettingsConfigDict

from app.services.constants import PATH_ENV_FILE


class Settings(BaseSettings):
    """Класс настроек проекта."""
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    model_config = SettingsConfigDict(env_file=PATH_ENV_FILE, extra="ignore")
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    @property
    def database_url(self) -> str:
        """Формирование URL для подключения БД."""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
