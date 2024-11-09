"""Database operations for the quality table."""

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.db.utils import handle_crud_operation
from aiventure.models import Quality, QualityBase


class QualityCRUD(BaseCRUD):
    """CRUD operations for the quality table."""

    @handle_crud_operation
    async def create(self, quality: QualityBase) -> Quality:
        """Create a new quality."""
        quality = Quality(**quality.model_dump())

        self.session.add(quality)
        await self.session.commit()
        await self.session.refresh(quality)

        return quality

    @handle_crud_operation
    async def get_by_id(self, quality_id: int) -> Quality | None:
        """Get a quality by id."""
        quality = await self.session.execute(select(Quality).where(col(Quality.id) == quality_id))
        return quality.scalar_one_or_none()

    @handle_crud_operation
    async def update(self, quality: QualityBase) -> Quality | None:
        """Update a quality."""
        _quality = await self.get_by_id(quality.id)

        if _quality is None:
            return None

        _quality.name = quality.name or _quality.name
        _quality.hex_color = quality.hex_color or _quality.hex_color

        self.session.add(_quality)
        await self.session.commit()
        await self.session.refresh(_quality)

        return _quality
