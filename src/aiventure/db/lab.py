"""Lab CRUD operations"""

from typing import Sequence

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Lab, LabBase


class LabCRUD(BaseCRUD):
    """CRUD operations for the lab table."""

    async def create(self, lab: LabBase) -> Lab:
        """Create a new lab."""
        lab = Lab(**lab.model_dump())

        self.session.add(lab)
        await self.session.commit()
        await self.session.refresh(lab)

        return lab

    async def get_by_id(self, lab_id: str) -> Lab | None:
        """Get a lab by id."""
        lab = await self.session.execute(select(Lab).where(col(Lab.id) == lab_id))
        return lab.scalar_one_or_none()

    async def get_by_player_id(self, player_id: str) -> Sequence[Lab]:
        """Get all labs by player id."""
        labs = await self.session.execute(select(Lab).where(col(Lab.player_id) == player_id))
        return labs.scalars().all()

    async def update(self) -> Lab | None:
        """Update a lab."""
        pass
