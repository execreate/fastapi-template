from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import settings


engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DB_ECHO_LOG,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
