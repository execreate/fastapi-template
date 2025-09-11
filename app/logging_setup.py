import logging


def setup_gunicorn_logging(logger_name: str = None) -> logging.Logger:
    """
    Route this app's logger to Gunicorn's error handlers when running under Gunicorn.
    Falls back to normal root logging otherwise.
    """
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app_logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()

    if gunicorn_logger.handlers:
        # re-use Gunicorn's handlers
        app_logger.handlers = gunicorn_logger.handlers
        app_logger.setLevel(gunicorn_logger.level)
        app_logger.propagate = False
    else:
        # Not under Gunicorn (e.g., local `uvicorn app:app`), keep default behavior
        if not app_logger.handlers:
            logging.basicConfig(level=logging.INFO)

    return app_logger
