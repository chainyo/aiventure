"""Player lab investment link crud."""

from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import PlayerLabInvestmentLink


class PlayerLabInvestmentLinkCRUD(BaseCRUD):
    """CRUD operations for the player lab investment link table."""

    async def create(self, player_id: str, lab_id: str, part: float) -> PlayerLabInvestmentLink:
        """Create a new player lab investment link."""
        link = PlayerLabInvestmentLink(player_id=player_id, lab_id=lab_id, part=part)

        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)

        return link

    async def update(self) -> PlayerLabInvestmentLink | None:
        """Update a player lab investment link."""
        pass

    async def get_by_player_id(self, player_id: str) -> Sequence[PlayerLabInvestmentLink]:
        """Get all player lab investment links by player id."""
        links = await self.session.execute(
            select(PlayerLabInvestmentLink).where(col(PlayerLabInvestmentLink.player_id) == player_id)
        )
        return links.scalars().all()

    async def get_by_lab_id(self, lab_id: str) -> Sequence[PlayerLabInvestmentLink]:
        """Get all player lab investment links by lab id."""
        links = await self.session.execute(
            select(PlayerLabInvestmentLink).where(col(PlayerLabInvestmentLink.lab_id) == lab_id)
        )
        return links.scalars().all()

    async def get_income_for_player(self, player_id: str) -> float | None:
        """Get the income for a player."""
        links = await self.session.execute(
            select(PlayerLabInvestmentLink)
            .where(col(PlayerLabInvestmentLink.player_id) == player_id)
            .options(selectinload(PlayerLabInvestmentLink.lab))
        )
        links = links.scalars().all()
        if links is None:
            return None

        return sum(link.part * link.lab.income for link in links)
