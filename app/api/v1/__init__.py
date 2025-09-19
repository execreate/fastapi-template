from fastapi import APIRouter

from .blog_post import router as blog_post_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(blog_post_router)
