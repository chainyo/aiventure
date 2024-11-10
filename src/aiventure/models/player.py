"""Player models."""

from typing import TYPE_CHECKING

from sqlmodel import Relationship
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.links import PlayerLabInvestmentLink


if TYPE_CHECKING:
    from aiventure.models.lab import Lab


class PlayerBase(UUIDModel):
    """Player model."""

    name: str
    funds: float

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "funds": 100000,
            }
        }
    )


class Player(PlayerBase, table=True):
    """Player model."""

    __tablename__ = "players"

    labs: list["Lab"] = Relationship(back_populates="player")
    investments: list["Lab"] = Relationship(back_populates="investors", link_model=PlayerLabInvestmentLink)
