import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class TimestampedBase:
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(), nullable=False, server_default=func.now())
    modified_at = Column(
        DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    __name__: str

    # so that created_at and modified_at columns can be accessed without querying the database
    __mapper_args__ = {"eager_defaults": True}

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
