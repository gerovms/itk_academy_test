from typing import Any, List, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class CRUDBase:

    def __init__(self, model: T) -> None:

        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[T]:

        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id,
            ),
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in: Any,
        session: AsyncSession,
    ) -> T:

        if hasattr(obj_in, "dict"):
            obj_in_data = obj_in.dict()
        else:
            obj_in_data = dict(obj_in) if isinstance(obj_in, dict) else {}
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
