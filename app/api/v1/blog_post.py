from uuid import UUID
from api.dependencies.database import DbSessionDep
from fastapi import APIRouter, Response, status
from schemas import blog_post as blog_post_schemas
from schemas.pagination import PaginationDep
from db.crud.blog_post import BlogPostCrud


router = APIRouter(
    prefix="/blog",
    tags=["Blog posts"],
)


@router.post("", status_code=201, response_model=blog_post_schemas.BlogPostSchema)
async def create_a_blog_post(
    blog_post: blog_post_schemas.InBlogPostSchema,
    db: DbSessionDep,
):
    crud = BlogPostCrud(db)
    result = await crud.create(blog_post)
    await crud.commit_session()
    return result


@router.get("", response_model=blog_post_schemas.PaginatedBlogPostSchema)
async def list_blog_posts(
    db: DbSessionDep,
    pagination: PaginationDep,
):
    crud = BlogPostCrud(db)
    return await crud.get_paginated_list(pagination.limit, pagination.offset)


@router.get(
    "/{post_id}",
    response_model=blog_post_schemas.BlogPostSchema,
    responses={
        404: {
            "description": "Object not found",
        },
    },
)
async def retrieve_a_blog_post(
    post_id: UUID,
    db: DbSessionDep,
):
    crud = BlogPostCrud(db)
    return await crud.get_by_id(post_id)


@router.patch(
    "/{post_id}",
    response_model=blog_post_schemas.BlogPostSchema,
    responses={
        404: {
            "description": "Object not found",
        },
    },
)
async def update_a_blog_post(
    post_id: UUID,
    blog_post: blog_post_schemas.UpdateBlogPostSchema,
    db: DbSessionDep,
):
    crud = BlogPostCrud(db)
    result = await crud.update_by_id(post_id, blog_post)
    await crud.commit_session()
    return result


@router.delete(
    "/{post_id}",
    status_code=204,
    responses={
        404: {
            "description": "Object not found",
        },
    },
)
async def delete_a_blog_post(
    post_id: UUID,
    db: DbSessionDep,
):
    crud = BlogPostCrud(db)
    await crud.delete_by_id(post_id)
    await crud.commit_session()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
