from core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DB_ECHO_LOG,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
