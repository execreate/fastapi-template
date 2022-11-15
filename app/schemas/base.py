from pydantic import BaseModel
from typing import Generic, TypeVar


class BaseSchema(BaseModel):
    class Config(BaseModel.Config):
        orm_mode = True


BASE_SCHEMA = TypeVar("BASE_SCHEMA", bound=BaseSchema)


class BasePaginatedSchema(BaseModel, Generic[BASE_SCHEMA]):
    total: int
    items: list[BASE_SCHEMA]

    class Config(BaseModel.Config):
        orm_mode = True
