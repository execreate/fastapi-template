import logging
import sys

from core.config import settings

logging_level = logging.INFO if not settings.DEBUG else logging.DEBUG
logging_format = "%(asctime)s | [%(levelname)s] | [%(name)s] %(message)s"
logging_date_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    stream=sys.stdout,
    level=logging_level,
    format=logging_format,
    datefmt=logging_date_format,
)


def setup_logging(logger_name: str = None) -> logging.Logger:
    """
    Set up logging configuration
    """
    app_logger = (
        logging.getLogger(logger_name) if logger_name else logging.getLogger("default")
    )
    app_logger.setLevel(level=logging_level)
    for handler in app_logger.handlers:
        handler.setFormatter(
            logging.Formatter(fmt=logging_format, datefmt=logging_date_format)
        )

    return app_logger
