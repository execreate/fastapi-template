import asyncio
from typing import Any, AsyncGenerator, Callable, Generator

import pytest_asyncio
from core.config import settings
from db.base import Base
from db.session import async_session
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncSession

from .setup_env import *  # noqa: setup test env


@pytest_asyncio.fixture(scope="session", autouse=True)
def setup_test_env(request):
    sync_engine = create_engine(
        str(settings.DATABASE_URL),
        echo=False,
    )

    with sync_engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)
        Base.metadata.create_all(bind=conn)

    def db_finalizer():
        with sync_engine.begin() as conn_:
            Base.metadata.drop_all(bind=conn_)

        sync_engine.dispose()

    request.addfinalizer(db_finalizer)


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
def override_get_session(db_session: AsyncSession) -> Callable:
    def override_get_session_():
        yield db_session

    return override_get_session_


@pytest_asyncio.fixture(scope="function")
def app_(override_get_session: Callable) -> FastAPI:
    from api.dependencies.database import get_db_session
    from main import app

    app.dependency_overrides[get_db_session] = override_get_session
    return app


@pytest_asyncio.fixture(scope="function")
async def async_client(app_: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        transport=ASGITransport(app=app_), base_url="http://localhost"
    ) as client:
        yield client
