import logging
import asyncio

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        engine = create_async_engine(settings.async_database_url)
        async with engine.connect() as conn:
            # Try to create session to check if DB is awake
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e
    await engine.dispose()


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())
