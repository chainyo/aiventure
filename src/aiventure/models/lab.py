"""Lab models."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.links import PlayerLabInvestmentLink
from aiventure.models.location import LocationEnum
from aiventure.models.player import Player


if TYPE_CHECKING:
    from aiventure.models.ai_model import AIModel
    from aiventure.models.employee import Employee


class LabBase(UUIDModel):
    """Lab model."""

    name: str
    location: LocationEnum
    valuation: float
    income: float
    tech_tree_id: str
    player_id: str = Field(foreign_key="players.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Lab Zero",
                "location": "us",
                "valuation": 1000000,
                "income": 100000,
                "tech_tree_id": "123e4567-e89b-12d3-a456-426614174001",
                "player_id": "123e4567-e89b-12d3-a456-426614174002",
            }
        }
    )


class Lab(LabBase, table=True):
    """Table for labs."""

    __tablename__ = "labs"

    employees: list["Employee"] = Relationship(back_populates="lab")
    models: list["AIModel"] = Relationship(back_populates="lab")
    investors: list[Player] = Relationship(back_populates="investments", link_model=PlayerLabInvestmentLink)
    player: Player = Relationship(back_populates="labs")
