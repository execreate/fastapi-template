from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session


async def get_db_session() -> AsyncGenerator[Any, Any]:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
