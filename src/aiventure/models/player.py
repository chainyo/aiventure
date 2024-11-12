"""Player models."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Relationship
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.links import PlayerLabInvestmentLink


if TYPE_CHECKING:
    from aiventure.models.lab import Lab, LabRead


class PlayerBase(UUIDModel):
    """Player model."""

    name: str
    funds: float
    user_id: str

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "funds": 100000,
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
            }
        }
    )


class Player(PlayerBase, table=True):
    """Player model."""

    __tablename__ = "players"

    labs: list["Lab"] = Relationship(back_populates="player")
    investments: list["Lab"] = Relationship(back_populates="investors", link_model=PlayerLabInvestmentLink)


class PlayerRead(BaseModel):
    """Player read model."""

    id: str
    name: str
    funds: float
    labs: list["LabRead"] | None
    investments: list["LabRead"] | None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "funds": 100000,
                "labs": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Lab Zero",
                        "location": "us",
                        "valuation": 1000000,
                        "income": 100000,
                        "tech_tree_id": "123e4567-e89b-12d3-a456-426614174001",
                        "player_id": "123e4567-e89b-12d3-a456-426614174002",
                        "employees": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174003",
                                "name": "Jane Doe",
                                "salary": 100000,
                                "image_url": "https://avatar.iran.liara.run/public",
                                "role_id": 1,
                                "quality_id": 1,
                                "modifiers": [],
                                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
                            }
                        ],
                        "models": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174004",
                                "name": "GPT-2",
                                "ai_model_type_id": 3,
                                "tech_tree_id": "123e4567-e89b-12d3-a456-426614174000",
                                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
                            }
                        ],
                        "investors": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174005",
                                "name": "Jill Doe",
                                "funds": 100000,
                                "labs": [],
                                "investments": [],
                            }
                        ],
                    }
                ],
                "investments": [
                    {
                        "player_id": "123e4567-e89b-12d3-a456-426614174000",
                        "lab_id": "123e4567-e89b-12d3-a456-426614174000",
                        "part": 0.5,
                    }
                ],
            }
        }
    )
