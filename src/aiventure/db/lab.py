"""Lab CRUD operations"""

from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Lab, LabBase, Player


class LabCRUD(BaseCRUD):
    """CRUD operations for the lab table."""

    async def create(self, lab: LabBase, player: Player) -> Lab:
        """Create a new lab."""
        lab = Lab(**lab.model_dump(), investors=[player])

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

    async def read_by_id(self, lab_id: str) -> Lab | None:
        """Read a lab by id."""
        lab = await self.session.execute(
            select(Lab)
            .where(col(Lab.id) == lab_id)
            .options(
                selectinload(Lab.player),
                selectinload(Lab.employees),
                selectinload(Lab.models),
                selectinload(Lab.investors),
            )
        )
        return lab.scalar_one_or_none()
