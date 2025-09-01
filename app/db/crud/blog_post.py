from typing import Type

from db.crud.base import BaseCrud
from db.tables.blog_post import BlogPost as BlogPostTable
from schemas.blog_post import (
    InBlogPostSchema,
    OutBlogPostSchema,
    PaginatedBlogPostSchema,
    UpdateBlogPostSchema,
)
from sqlalchemy.sql.elements import UnaryExpression


class BlogPostCrud(
    BaseCrud[
        InBlogPostSchema,
        UpdateBlogPostSchema,
        OutBlogPostSchema,
        PaginatedBlogPostSchema,
        BlogPostTable,
    ]
):
    @property
    def _table(self) -> Type[BlogPostTable]:
        return BlogPostTable

    @property
    def _out_schema(self) -> Type[OutBlogPostSchema]:
        return OutBlogPostSchema

    @property
    def default_ordering(self) -> UnaryExpression:
        return BlogPostTable.created_at.desc()

    @property
    def _paginated_schema(self) -> Type[PaginatedBlogPostSchema]:
        return PaginatedBlogPostSchema
