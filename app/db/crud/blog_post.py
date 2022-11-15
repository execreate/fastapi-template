from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import InstrumentedAttribute

from db.crud.base import BaseCrud
from db.tables.blog_post import BlogPost
from schemas.blog_post import (
    InBlogPostSchema,
    UpdateBlogPostSchema,
    BlogPostSchema,
    PaginatedBlogPostSchema,
)


class BlogPostCrud(
    BaseCrud[
        InBlogPostSchema,
        UpdateBlogPostSchema,
        BlogPostSchema,
        PaginatedBlogPostSchema,
        BlogPost,
    ]
):
    @property
    def _table(self) -> Type[BlogPost]:
        return BlogPost

    @property
    def _schema(self) -> Type[BlogPostSchema]:
        return BlogPostSchema

    @property
    def _order_by(self) -> InstrumentedAttribute:
        return desc(BlogPost.created_at)

    @property
    def _paginated_schema(self) -> Type[PaginatedBlogPostSchema]:
        return PaginatedBlogPostSchema
