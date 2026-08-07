"""Persistence ports shared by future bounded contexts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import Base

ModelT = TypeVar("ModelT", bound=Base)
IdT = TypeVar("IdT")


class AbstractRepository[ModelT: Base, IdT](ABC):
    """Minimal repository contract; domain-specific queries belong downstream."""

    @abstractmethod
    async def get(self, identity: IdT) -> ModelT | None: ...

    @abstractmethod
    async def add(self, entity: ModelT) -> ModelT: ...


class SQLAlchemyRepository(AbstractRepository[ModelT, IdT]):
    """Generic SQLAlchemy implementation for simple entity operations."""

    model_type: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, identity: IdT) -> ModelT | None:
        return await self.session.get(self.model_type, identity)

    async def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[ModelT]:
        result = await self.session.scalars(
            select(self.model_type).offset(offset).limit(limit)
        )
        return list(result.all())
