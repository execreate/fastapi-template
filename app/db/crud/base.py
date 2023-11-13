import abc
import logging
from typing import Generic, TypeVar, Type
from fastapi import HTTPException

from sqlalchemy import func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute
from core.config import settings, EnvironmentEnum
from schemas.base import BaseSchema, BasePaginatedSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseSchema)
PARTIAL_UPDATE_SCHEMA = TypeVar("PARTIAL_UPDATE_SCHEMA", bound=BaseSchema)
PAGINATED_SCHEMA = TypeVar("PAGINATED_SCHEMA", bound=BasePaginatedSchema)
TABLE = TypeVar("TABLE")


logger = logging.getLogger(__name__)


class BaseCrud(
    Generic[IN_SCHEMA, PARTIAL_UPDATE_SCHEMA, OUT_SCHEMA, PAGINATED_SCHEMA, TABLE],
    metaclass=abc.ABCMeta,
):
    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    async def commit_session(self):
        """
        Commits the session if not in testing environment
        :return: None
        """
        if settings.ENVIRONMENT == EnvironmentEnum.TEST:
            await self._db_session.flush()
            return

        await self._db_session.commit()

    def get_active_statement(self, stmt: any, active_only: bool):
        if active_only:
            return stmt.where(self._table.is_active)
        return stmt

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abc.abstractmethod
    def _out_schema(self) -> Type[OUT_SCHEMA]:
        ...

    @property
    @abc.abstractmethod
    def default_ordering(self) -> InstrumentedAttribute:
        ...

    @property
    @abc.abstractmethod
    def _paginated_schema(self) -> Type[PAGINATED_SCHEMA]:
        ...

    async def create(self, in_schema: IN_SCHEMA) -> OUT_SCHEMA:
        entry = self._table(**in_schema.model_dump())
        self._db_session.add(entry)
        await self._db_session.flush()
        return self._out_schema.model_validate(entry)

    async def get_by_id(self, entry_id, active_only=True) -> OUT_SCHEMA:
        result = await self._db_session.execute(
            self.get_active_statement(
                select(self._table).where(self._table.id == entry_id), active_only
            )
        )
        entry = result.scalar_one_or_none()
        if not entry:
            raise HTTPException(status_code=404, detail="Object not found")
        return self._out_schema.model_validate(entry)

    async def update_by_id(
        self, entry_id, in_data: PARTIAL_UPDATE_SCHEMA, active_only=True
    ) -> OUT_SCHEMA:
        result = await self._db_session.execute(
            self.get_active_statement(
                select(self._table).where(self._table.id == entry_id), active_only
            )
        )
        entry = result.scalar_one_or_none()
        if not entry:
            raise HTTPException(status_code=404, detail="Object not found")
        in_data_dict: dict = in_data.model_dump(exclude_unset=True)
        for _k, _v in in_data_dict.items():
            setattr(entry, _k, _v)
        await self._db_session.flush()
        return self._out_schema.model_validate(entry)

    async def delete_by_id(self, entry_id, permanently=False) -> None:
        result = await self._db_session.execute(
            select(self._table).where(self._table.id == entry_id)
        )
        entry = result.scalar_one_or_none()
        if not entry or (not entry.is_active and not permanently):
            raise HTTPException(status_code=404, detail="Object not found")

        if permanently:
            await self._db_session.delete(entry)
        else:
            entry.is_active = False

        await self._db_session.flush()
        return

    async def get_paginated_list(
        self,
        limit: int,
        offset: int,
        order_by: UnaryExpression = None,
        active_only=True,
    ) -> PAGINATED_SCHEMA:
        if order_by is None:
            order_by = self.default_ordering
        result: Result = await self._db_session.execute(
            self.get_active_statement(select(self._table), active_only)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        entries = result.scalars()
        total_count: Result = await self._db_session.execute(
            self.get_active_statement(
                select(func.count()).select_from(self._table), active_only
            )
        )
        return self._paginated_schema(
            total=total_count.scalar(),
            items=[self._out_schema.model_validate(entry) for entry in entries],
        )
