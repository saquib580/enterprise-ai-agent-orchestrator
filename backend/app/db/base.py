"""Shared SQLAlchemy declarative base and model mixins."""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Base metadata registry for ORM models."""


class TimestampMixin:
    """Add server-managed creation and update timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class TenantScopingMixin:
    """Add a mandatory indexed tenant identifier."""

    @declared_attr
    def tenant_id(cls) -> Mapped[int]:
        return mapped_column(Integer, nullable=False, index=True)


class BaseModel(Base, TimestampMixin):
    """Common integer primary key and timestamp fields."""

    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self) -> dict[str, Any]:
        """Return mapped column values for internal serialization."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
