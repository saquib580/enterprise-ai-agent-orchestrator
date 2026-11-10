"""Generic asynchronous repository with tenant-safe access patterns."""

from abc import ABC
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(ABC, Generic[ModelT]):
    """Reusable reads and create operation; caller owns transaction commit."""

    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get(self, entity_id: int, *, tenant_id: int | None = None) -> ModelT | None:
        """Retrieve an entity; tenant-owned models require tenant_id."""
        statement = select(self.model).where(self.model.id == entity_id)
        if hasattr(self.model, "tenant_id"):
            if tenant_id is None:
                raise ValueError("tenant_id is required for tenant-owned models")
            statement = statement.where(getattr(self.model, "tenant_id") == tenant_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list(
        self, skip: int = 0, limit: int = 100, *, tenant_id: int | None = None
    ) -> list[ModelT]:
        """Return bounded, ordered records."""
        if skip < 0:
            raise ValueError("skip cannot be negative")
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        statement = select(self.model).order_by(self.model.id).offset(skip).limit(limit)
        if hasattr(self.model, "tenant_id"):
            if tenant_id is None:
                raise ValueError("tenant_id is required for tenant-owned models")
            statement = statement.where(getattr(self.model, "tenant_id") == tenant_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, *, tenant_id: int | None = None, **values: Any) -> ModelT:
        """Add and flush an entity without committing the caller transaction."""
        if hasattr(self.model, "tenant_id"):
            if tenant_id is None:
                raise ValueError("tenant_id is required for tenant-owned models")
            values["tenant_id"] = tenant_id
        entity = self.model(**values)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
