from core.config import settings
from fastapi import APIRouter

from .blog_post import router as blog_post_router

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(blog_post_router)
