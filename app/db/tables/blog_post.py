from db.base_class import TimestampedBase
from sqlalchemy.orm import Mapped, mapped_column


class BlogPost(TimestampedBase):
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
