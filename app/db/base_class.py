import datetime
import uuid

from sqlalchemy import func, DateTime
from sqlalchemy.orm import as_declarative, declared_attr, mapped_column, Mapped


@as_declarative()
class TimestampedBase:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, server_default=func.now()
    )
    modified_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    __name__: str

    # so that created_at and modified_at columns can be accessed without querying the database
    __mapper_args__ = {"eager_defaults": True}

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
