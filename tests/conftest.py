import sys
import asyncio
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import app
from app.core.db import Base, get_async_session
from app.crud.user import user_crud

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(async_engine):
    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_async_session] = lambda: db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def get_token(client, username, password):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password}
        )
    return resp.json()["access_token"]


@pytest.fixture
async def test_user(db_session, client):
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "123456"
    user = await user_crud.create_user(
        username=username,
        password=password,
        session=db_session
        )
    await db_session.commit()
    token = await get_token(client, username, password)
    return {
        "username": username,
        "password": password,
        "id": user.id,
        "wallet_id": user.wallet.id,
        "auth_headers": {"Authorization": f"Bearer {token}"}
    }


@pytest.fixture
async def another_user(db_session, client):
    username = f"otheruser_{uuid.uuid4().hex[:8]}"
    password = "123456"
    user = await user_crud.create_user(
        username=username,
        password=password,
        session=db_session
        )
    await db_session.commit()
    token = await get_token(client, username, password)
    return {
        "username": username,
        "password": password,
        "id": user.id,
        "wallet_id": user.wallet.id,
        "auth_headers": {"Authorization": f"Bearer {token}"}
    }
