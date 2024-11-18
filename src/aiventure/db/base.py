"""Base module for the database."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD(ABC):
    """Base CRUD class."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the base CRUD class."""
        self.session = session

    async def __aenter__(self) -> BaseCRUD:
        """Enter the context manager."""
        return self

    async def __aexit__(
        self, exc_type: type | None, exc_value: Exception | None, traceback: TracebackType | None
    ) -> None:
        """Exit the context manager."""
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()

    @abstractmethod
    async def create(self, model: BaseModel) -> Any:
        """Create a new model."""
        pass

    @abstractmethod
    async def update(self, model: BaseModel) -> Any:
        """Update an existing model."""
        pass
