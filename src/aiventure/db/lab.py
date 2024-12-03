"""Lab CRUD operations"""

from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Lab, LabBase, Player, PlayerLabInvestmentLink


class LabCRUD(BaseCRUD):
    """CRUD operations for the lab table."""

    async def create(self, lab: LabBase, player: Player) -> Lab:
        """Create a new lab."""
        lab_link = PlayerLabInvestmentLink(player=player, lab=Lab(**lab.model_dump()), part=1.0)

        self.session.add(lab_link)
        await self.session.commit()
        await self.session.refresh(lab_link)

        # We retrieve the full lab from the database to expose created data to the client
        lab = await self.read_by_id(lab_link.lab_id)
        if not lab:
            raise ValueError("Lab not found")

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

    async def read_all_for_leaderboard(self) -> Sequence[Lab]:
        """Read all labs for the leaderboard."""
        labs = await self.session.execute(
            select(Lab)
            .order_by(col(Lab.valuation).desc())
            .options(
                selectinload(Lab.player),
                selectinload(Lab.employees),
                selectinload(Lab.models),
                selectinload(Lab.investors),
            )
            .limit(100)
        )
        return labs.scalars().all()

    async def update_valuation(self, lab_id: str) -> Lab | None:
        """Update the valuation of a lab."""
        lab = await self.read_by_id(lab_id)
        if lab:
            lab.valuation = lab.calculate_valuation()
            await self.session.commit()
            await self.session.refresh(lab)

        return lab

    async def update_income(self, lab_id: str) -> Lab | None:
        """Update the income of a lab."""
        lab = await self.read_by_id(lab_id)
        if lab:
            lab.income = lab.calculate_income()
            await self.session.commit()
            await self.session.refresh(lab)

        return lab
