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

root = logging.getLogger()
root.setLevel(logging_level)

# set the formatter for the stdout handler
formatter = logging.Formatter(fmt=logging_format, datefmt=logging_date_format)
if root.handlers:
    root.handlers[0].setFormatter(formatter)


def setup_logging(logger_name: str = None) -> logging.Logger:
    app_logger = (
        logging.getLogger(logger_name) if logger_name else logging.getLogger("default")
    )
    app_logger.setLevel(level=logging_level)

    return app_logger
