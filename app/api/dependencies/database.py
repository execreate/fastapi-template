from typing import Annotated, Any, AsyncGenerator

from db.session import async_session
from fastapi import Depends
from logging_setup import setup_gunicorn_logging
from sqlalchemy.ext.asyncio import AsyncSession

logger = setup_gunicorn_logging(__name__)


async def get_db_session() -> AsyncGenerator[Any, Any]:
    """
    Dependency function that yields db sessions
    """
    logger.info("Creating new db session")
    async with async_session() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
