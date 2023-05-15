import pytest
import json
from httpx import AsyncClient, QueryParams
from schemas.blog_post import InBlogPostSchema, OutBlogPostSchema
from sqlalchemy.ext.asyncio import AsyncSession
from .factory.blog_post_factory import BlogPostFactory
from .utils import dicts_are_equal


@pytest.mark.asyncio
async def test_create_a_blog_post(async_client: AsyncClient):
    blog_post_input = InBlogPostSchema(
        title="Hello world!",
        body="This is my first blog post and I'm really excited to have so many followers!",
    )
    response = await async_client.post(
        "/v1/blog",
        json=blog_post_input.dict(),
    )
    response_data: dict = response.json()

    assert response.status_code == 201
    assert dicts_are_equal(
        response_data, blog_post_input.dict(), for_keys={"title", "body"}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "total_posts,limit_param,offset_param",
    [(10, 5, 0), (5, 5, 2), (25, 10, 10), (25, 15, 13)],
)
async def test_list_blog_posts(
    async_client: AsyncClient,
    db_session: AsyncSession,
    total_posts: int,
    limit_param: int,
    offset_param: int,
):
    db_session.add_all(BlogPostFactory.build_batch(total_posts))
    await db_session.flush()

    response = await async_client.get(
        "/v1/blog", params=QueryParams(limit=limit_param, offset=offset_param)
    )
    response_data: dict = response.json()

    assert response_data["total"] == total_posts
    assert isinstance(response_data["items"], list)
    assert len(response_data["items"]) == min(
        max(total_posts - offset_param, 0),
        limit_param,
    )


@pytest.mark.asyncio
async def test_retrieve_a_blog_post(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    post = BlogPostFactory.build()
    db_session.add(post)
    await db_session.flush()

    response = await async_client.get(f"/v1/blog/{post.id}")
    response_data: dict = response.json()

    assert response.status_code == 200
    assert OutBlogPostSchema.from_orm(post).json() == json.dumps(response_data)


@pytest.mark.asyncio
async def test_update_a_blog_post(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    post = BlogPostFactory.build()
    db_session.add(post)
    await db_session.flush()

    data = {"title": "Awesome new title"}
    response = await async_client.patch(f"/v1/blog/{post.id}", json=data)
    response_data: dict = response.json()

    assert response.status_code == 200
    assert dicts_are_equal(data, response_data, for_keys={"title"})


@pytest.mark.asyncio
async def test_delete_a_blog_post(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    post = BlogPostFactory.build()
    db_session.add(post)
    await db_session.flush()

    response = await async_client.delete(f"/v1/blog/{post.id}")
    assert response.status_code == 204

    response = await async_client.get(f"/v1/blog/{post.id}")
    assert response.status_code == 404
