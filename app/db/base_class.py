import re
import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.orm import as_declarative, declared_attr, mapped_column, Mapped
from core.config import settings, EnvironmentEnum


def camel_to_snake(name):
    """
    Convert camel case to snake case and lowercase the result
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


@as_declarative()
class TimestampedBase:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    modified_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )
    __name__: str

    # so that created_at and modified_at columns can be accessed without querying the database
    __mapper_args__ = {"eager_defaults": True}

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        if settings.ENVIRONMENT == EnvironmentEnum.TEST:
            return f"test_{camel_to_snake(cls.__name__)}"

        return camel_to_snake(cls.__name__)
