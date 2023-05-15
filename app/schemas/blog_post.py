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


class OutBlogPostSchema(BlogPostSchemaBase):
    id: UUID
    created_at: datetime
    modified_at: datetime


class PaginatedBlogPostSchema(BasePaginatedSchema[OutBlogPostSchema]):
    items: list[OutBlogPostSchema]
