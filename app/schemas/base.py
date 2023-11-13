from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


BASE_SCHEMA = TypeVar("BASE_SCHEMA", bound=BaseSchema)


class BasePaginatedSchema(BaseModel, Generic[BASE_SCHEMA]):
    total: int
    items: list[BASE_SCHEMA]

    model_config = ConfigDict(from_attributes=True)
