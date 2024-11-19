"""Base module for the database."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound="BaseCRUD")


class BaseCRUD(ABC):
    """Base CRUD class."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the base CRUD class."""
        self.session = session

    async def __aenter__(self: T) -> T:
        """Enter the context manager."""
        return self

    async def __aexit__(
        self, exc_type: type | None, exc_value: Exception | None, traceback: TracebackType | None
    ) -> None:
        """Exit the context manager."""
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def rollback(self) -> None:
        """Rollback the session."""
        await self.session.rollback()

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> Any:
        """Create a new model."""
        pass

    @abstractmethod
    async def update(self, *args: Any, **kwargs: Any) -> Any:
        """Update an existing model."""
        pass
