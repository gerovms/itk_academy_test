from typing import AsyncGenerator
import logging

from fastapi import HTTPException
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column as mp

from app.core.config import settings


class PreBase:
    id: Mapped[int] = mp(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as async_session:
        logging.info("Открытие новой сессии базы данных.")
        try:
            yield async_session
            await async_session.commit()
            logging.info(
                "Сессия завершена и изменения в базе данных зафиксированы.",
            )
        except HTTPException as http_exc:
            logging.error(f"HTTPException в сессии: {http_exc}")
            await async_session.rollback()
            raise http_exc
        except Exception as err:
            logging.error(f"Ошибка в сессии: {err}")
            await async_session.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            logging.info("Сессия закрыта.")
