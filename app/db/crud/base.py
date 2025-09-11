import abc
from typing import Generic, Type, TypeVar

from core.config import EnvironmentEnum, settings
from db.base_class import TimestampedBase
from fastapi import HTTPException
from logging_setup import setup_gunicorn_logging
from schemas.base import BasePaginatedSchema, BaseSchema
from sqlalchemy import ColumnClause, column, delete, func, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import Select, Update
from sqlalchemy.sql.elements import UnaryExpression

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseSchema)
PARTIAL_UPDATE_SCHEMA = TypeVar("PARTIAL_UPDATE_SCHEMA", bound=BaseSchema)
PAGINATED_SCHEMA = TypeVar("PAGINATED_SCHEMA", bound=BasePaginatedSchema)
TABLE = TypeVar("TABLE", bound=TimestampedBase)
S = TypeVar("S", Select, Update)

logger = setup_gunicorn_logging(__name__)


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
        logger.info("Committing session...")
        if settings.ENVIRONMENT == EnvironmentEnum.TEST:
            logger.info("Skipping session.commit() in test environment")
            await self._db_session.flush()
            return

        await self._db_session.commit()

    def apply_active_statement(self, stmt: S, active_only: bool) -> S:
        if active_only:
            return stmt.where(self._table.deleted_at.is_(None))
        return stmt

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]: ...

    @property
    @abc.abstractmethod
    def _out_schema(self) -> Type[OUT_SCHEMA]: ...

    @property
    @abc.abstractmethod
    def default_ordering(self) -> InstrumentedAttribute: ...

    @property
    @abc.abstractmethod
    def _paginated_schema(self) -> Type[PAGINATED_SCHEMA]: ...

    @property
    def out_schema_columns(self) -> list[ColumnClause]:
        return [column(i) for i in self._out_schema.model_fields.keys()]

    async def create(self, in_schema: IN_SCHEMA) -> OUT_SCHEMA:
        entry = self._table(**in_schema.model_dump())
        self._db_session.add(entry)
        await self._db_session.flush()
        return self._out_schema.model_validate(entry)

    async def get_by_id(self, entry_id, active_only=True) -> OUT_SCHEMA:
        result = await self._db_session.execute(
            self.apply_active_statement(
                select(*self.out_schema_columns)
                .select_from(self._table)
                .where(self._table.id == entry_id),
                active_only,
            )
        )
        entry = result.first()
        if not entry:
            raise HTTPException(status_code=404, detail="Object not found")
        return self._out_schema.model_validate(entry)

    async def update_by_id(
        self, entry_id, in_data: PARTIAL_UPDATE_SCHEMA, active_only=True, raise_404=True
    ) -> None:
        result = await self._db_session.execute(
            self.apply_active_statement(
                update(self._table).where(self._table.id == entry_id), active_only
            ).values(**in_data.model_dump(exclude_unset=True))
        )
        if result.rowcount == 0 and raise_404:
            raise HTTPException(status_code=404, detail="Object not found")
        await self._db_session.flush()
        return

    async def delete_by_id(self, entry_id, permanently=False, raise_404=True) -> None:
        stmt = delete(self._table).where(self._table.id == entry_id)
        if not permanently:
            stmt = self.apply_active_statement(
                update(self._table).where(self._table.id == entry_id), True
            ).values(deleted_at=func.current_timestamp())

        result = await self._db_session.execute(stmt)
        if result.rowcount == 0 and raise_404:  # noqa
            raise HTTPException(status_code=404, detail="Object not found")

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
            self.apply_active_statement(
                select(*self.out_schema_columns).select_from(self._table), active_only
            )
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        entries = result.all()
        total_count: Result = await self._db_session.execute(
            self.apply_active_statement(
                select(func.count()).select_from(self._table), active_only
            )
        )
        return self._paginated_schema(
            total=total_count.scalar(),
            items=[self._out_schema.model_validate(entry) for entry in entries],
        )
