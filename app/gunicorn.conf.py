import logging

from hyperdx.opentelemetry import configure_opentelemetry


def post_fork(server, worker):
    # here we set up OTEL instrumentation for the app
    gunicorn_logger = logging.getLogger("gunicorn.error")

    gunicorn_logger.info("Configuring OpenTelemetry for the app")
    configure_opentelemetry()

    otel_handler = gunicorn_logger.root.handlers[-1]
    gunicorn_logger.addHandler(otel_handler)
