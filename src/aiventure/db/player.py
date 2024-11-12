"""Database operations for the player table."""

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.db.utils import handle_crud_operation
from aiventure.models import Player, PlayerBase, PlayerRead


class PlayerCRUD(BaseCRUD):
    """CRUD operations for the player table."""

    @handle_crud_operation
    async def create(self, player: PlayerBase) -> Player:
        """Create a new player."""
        player = Player(**player.model_dump())

        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)

        return player

    @handle_crud_operation
    async def get_by_id(self, player_id: str) -> Player | None:
        """Get a player by id."""
        player = await self.session.execute(select(Player).where(col(Player.id) == player_id))
        return player.scalar_one_or_none()

    @handle_crud_operation
    async def get_by_user_id(self, user_id: str) -> Player | None:
        """Get a player by user id."""
        player = await self.session.execute(select(Player).where(col(Player.user_id) == user_id))
        return player.scalar_one_or_none()

    @handle_crud_operation
    async def update(self, player: PlayerBase) -> Player | None:
        """Update a player."""
        _player = await self.get_by_id(player.id)

        if _player is None:
            return None

        _player.name = player.name or _player.name
        _player.funds = player.funds or _player.funds

        self.session.add(_player)
        await self.session.commit()
        await self.session.refresh(_player)

        return _player

    @handle_crud_operation
    async def read_by_id(self, player_id: str) -> PlayerRead | None:
        """Read a player by id."""
        _player = await self.get_by_id(player_id)
        return PlayerRead.model_validate(_player) if _player else None

    @handle_crud_operation
    async def read_by_user_id(self, user_id: str) -> PlayerRead | None:
        """Read a player by user id."""
        _player = await self.get_by_user_id(user_id)
        return PlayerRead.model_validate(_player) if _player else None
