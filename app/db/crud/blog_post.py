from typing import Type

from sqlalchemy.sql.elements import UnaryExpression

from db.crud.base import BaseCrud
from db.tables.blog_post import BlogPost
from schemas.blog_post import (
    InBlogPostSchema,
    UpdateBlogPostSchema,
    OutBlogPostSchema,
    PaginatedBlogPostSchema,
)


class BlogPostCrud(
    BaseCrud[
        InBlogPostSchema,
        UpdateBlogPostSchema,
        OutBlogPostSchema,
        PaginatedBlogPostSchema,
        BlogPost,
    ]
):
    @property
    def _table(self) -> Type[BlogPost]:
        return BlogPost

    @property
    def _out_schema(self) -> Type[OutBlogPostSchema]:
        return OutBlogPostSchema

    @property
    def _default_ordering(self) -> UnaryExpression:
        return BlogPost.created_at.desc()

    @property
    def _paginated_schema(self) -> Type[PaginatedBlogPostSchema]:
        return PaginatedBlogPostSchema
