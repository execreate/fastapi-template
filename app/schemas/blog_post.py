from uuid import UUID
from datetime import datetime
from schemas.base import BaseSchema, BasePaginatedSchema


class BlogPostSchemaBase(BaseSchema):
    title: str
    body: str


class UpdateBlogPostSchema(BaseSchema):
    title: str = ""
    body: str = ""


class InBlogPostSchema(BlogPostSchemaBase):
    ...


class BlogPostSchema(BlogPostSchemaBase):
    id: UUID
    created_at: datetime
    modified_at: datetime


class PaginatedBlogPostSchema(BasePaginatedSchema[BlogPostSchema]):
    items: list[BlogPostSchema]
