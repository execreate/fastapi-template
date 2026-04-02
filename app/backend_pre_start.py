import asyncio
import logging

from sqlalchemy.sql import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from db.session import async_session
from logging_setup import setup_logging

logger = setup_logging("backend_pre_start")

max_tries = 30 * 5  # 5 minutes
wait_seconds = 2


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        async with async_session() as session:
            # Try to create a session to check if DB is awake
            await session.execute(text("SELECT 1"))
    except Exception as e:
        logger.error("failed to connect to the database", exc_info=e)
        raise e


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())
