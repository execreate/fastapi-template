from sqlalchemy import Column, String

from db.base_class import TimestampedBase


class BlogPost(TimestampedBase):
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
