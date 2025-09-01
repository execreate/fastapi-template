import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi

from api import v1
from api.dependencies.docs_security import basic_http_credentials
from core.config import settings
from db.session import engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

description = """
FastAPI template project 🚀
"""
version = "v0.0.1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os, sys

    if "PYTHONPATH" not in os.environ:
        os.environ["PYTHONPATH"] = ":".join(sys.path)
    try:
        import opentelemetry.instrumentation.auto_instrumentation.sitecustomize  # noqa

        logger.debug("OpenTelemetry initialized")
    except ImportError:
        logger.warning("OpenTelemetry not initialized!")

    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version=version,
    lifespan=lifespan,
    contact={
        "name": "Jorilla Abdullaev",
        "url": "https://jorilla.t.me",
        "email": "jorilla.abdullaev@protonmail.com",
    },
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)

# include routes here
app.include_router(v1.api_router)


@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: str = Depends(basic_http_credentials)):
    schema = get_openapi(
        title=settings.PROJECT_NAME + " | API Documentation",
        description=description,
        routes=app.routes,
        version=version,
    )
    # schema["info"]["x-logo"] = {
    #     "url": "https://YOUR_WEBSITE/logo.svg",
    #     "href": "https://YOUR_WEBSITE/",
    #     "backgroundColor": "#fff",
    #     "altText": "YOUR BRAND NAME",
    # }
    return schema


@app.get(
    "/docs", include_in_schema=False, dependencies=[Depends(basic_http_credentials)]
)
async def get_redoc_documentation():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="FastAPI | Documentation",
        # redoc_favicon_url="https://YOUR_WEBSITE/favicon.ico",
    )


@app.get("/health")
@app.head("/health")
async def health_check() -> str:
    return "OK"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level=logging.DEBUG)
