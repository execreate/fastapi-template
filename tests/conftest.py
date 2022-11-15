import os
import asyncio
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator, Callable

from db.session import async_session, engine


os.environ.setdefault("ENVIRONMENT", "test")


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async with engine.begin() as conn:
        async with async_session(bind=conn) as session:
            yield session
            await session.rollback()


@pytest_asyncio.fixture(scope="function")
def override_get_session(db_session: AsyncSession) -> Callable:
    def override_get_session_():
        yield db_session

    return override_get_session_


@pytest_asyncio.fixture(scope="function")
def app_(override_get_session: Callable) -> FastAPI:
    from main import app
    from api.dependencies.database import get_db_session

    app.dependency_overrides[get_db_session] = override_get_session
    return app


@pytest_asyncio.fixture(scope="function")
async def async_client(app_: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app_, base_url="http://test") as client:
        yield client
