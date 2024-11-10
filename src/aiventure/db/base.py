"""Base module for the database."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD(ABC):
    """Base CRUD class."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the base CRUD class."""
        self.session = session

    @abstractmethod
    async def create(self, model: BaseModel) -> Any:
        """Create a new model."""
        pass

    @abstractmethod
    async def update(self, model: BaseModel) -> Any:
        """Update an existing model."""
        pass
