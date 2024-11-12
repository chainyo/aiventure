"""Lab models."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.links import PlayerLabInvestmentLink
from aiventure.models.location import LocationEnum


if TYPE_CHECKING:
    from aiventure.models.ai_model import AIModel, AIModelRead
    from aiventure.models.employee import Employee, EmployeeRead
    from aiventure.models.player import Player, PlayerRead


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
    investors: list["Player"] = Relationship(back_populates="investments", link_model=PlayerLabInvestmentLink)
    player: "Player" = Relationship(back_populates="labs")


class LabRead(BaseModel):
    """Lab read model."""

    id: str
    name: str
    location: LocationEnum
    valuation: float
    income: float
    tech_tree_id: str
    player_id: str
    employees: list["EmployeeRead"]
    models: list["AIModelRead"]
    investors: list["PlayerRead"]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
                        "name": "John Doe",
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
                        "name": "John Doe",
                        "funds": 100000,
                        "labs": [],
                        "investments": [],
                    }
                ],
            }
        }
    )
