from datetime import datetime

from schemas.base import BasePaginatedSchema, BaseSchema


class BlogPostSchemaBase(BaseSchema):
    title: str
    body: str


class UpdateBlogPostSchema(BaseSchema):
    title: str = ""
    body: str = ""


class InBlogPostSchema(BlogPostSchemaBase): ...


class OutBlogPostSchema(BlogPostSchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime


class PaginatedBlogPostSchema(BasePaginatedSchema[OutBlogPostSchema]): ...
