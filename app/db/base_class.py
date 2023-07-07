import re
import datetime

from sqlalchemy import func
from sqlalchemy.sql import expression
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
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    modified_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False, server_default=expression.true()
    )
    __name__: str

    # so that created_at and modified_at columns can be accessed without querying the database
    __mapper_args__ = {"eager_defaults": True}

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        default_name = camel_to_snake(cls.__name__)
        if settings.ENVIRONMENT == EnvironmentEnum.TEST:
            return f"test_{default_name}"

        return default_name
