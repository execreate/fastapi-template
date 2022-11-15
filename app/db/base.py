# Import all the models, so that TimestampedBase has them before being imported by Alembic

from db.base_class import TimestampedBase as Base  # noqa: F401
from db.tables.blog_post import BlogPost  # noqa: F401
