"""Game models."""

from pydantic import BaseModel


class GlobalGameState(BaseModel):
    """Global game state."""

    n_connected_players: int
