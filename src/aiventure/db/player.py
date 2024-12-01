"""Database operations for the player table."""

from sqlalchemy.orm import selectinload
from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Player, PlayerBase


class PlayerCRUD(BaseCRUD):
    """CRUD operations for the player table."""

    async def create(self, player: PlayerBase) -> Player:
        """Create a new player."""
        player = Player(**player.model_dump())

        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)

        return player

    async def get_by_id(self, player_id: str) -> Player | None:
        """Get a player by id."""
        player = await self.session.execute(select(Player).where(col(Player.id) == player_id))
        return player.scalar_one_or_none()

    async def get_by_user_id(self, user_id: str) -> Player | None:
        """Get a player by user id."""
        player = await self.session.execute(select(Player).where(col(Player.user_id) == user_id))
        return player.scalar_one_or_none()

    async def update(self, player: PlayerBase) -> Player | None:
        """Update a player."""
        _player = await self.get_by_user_id(player.user_id)

        if _player is None:
            return None

        _player.name = player.name or _player.name
        _player.funds = player.funds or _player.funds

        self.session.add(_player)
        await self.session.commit()
        await self.session.refresh(_player)

        return _player

    async def increment_funds(self, player_id: str, amount: int) -> Player | None:
        """Increment a player's funds."""
        _player = await self.get_by_id(player_id)

        if _player is None:
            return None

        _player.funds += amount

        self.session.add(_player)
        await self.session.commit()
        await self.session.refresh(_player)

        return _player

    async def decrement_funds(self, player_id: str, amount: int) -> Player | None:
        """Decrement a player's funds."""
        _player = await self.get_by_id(player_id)

        if _player is None:
            return None

        _player.funds -= amount

        self.session.add(_player)
        await self.session.commit()
        await self.session.refresh(_player)

        return _player

    async def read_player_data_by_id(self, player_id: str) -> Player | None:
        """Read player data by id."""
        query = (
            select(Player)
            .where(col(Player.id) == player_id)
            .options(selectinload(Player.labs), selectinload(Player.investments))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def read_player_data_by_user_id(self, user_id: str) -> Player | None:
        """Read player data by user id."""
        query = (
            select(Player)
            .where(col(Player.user_id) == user_id)
            .options(selectinload(Player.labs), selectinload(Player.investments))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
