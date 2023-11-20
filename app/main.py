from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from api.dependencies.docs_security import basic_http_credentials

from db.session import engine

from api import v1

description = """
FastAPI template project 🚀
"""
version = "v0.0.1"


@asynccontextmanager
async def lifespan(app: FastAPI):
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Accept-Language"],
)
