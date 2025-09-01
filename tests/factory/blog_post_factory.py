from db.tables.blog_post import BlogPost as BlogPostTable

from .base_factories import TimeStampedFactory


class BlogPostFactory(TimeStampedFactory):
    class Meta:
        model = BlogPostTable

    title = "blog post title"
    body = "really long blog post body text"
