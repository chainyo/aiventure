"""Links tables for many-to-many relationships."""

from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig


class EmployeeModifierLink(SQLModel, table=True):
    """Link table for employees and modifiers."""

    __tablename__ = "employee_modifier_link"

    employee_id: str | None = Field(default=None, foreign_key="employees.id", primary_key=True)
    modifier_id: str | None = Field(default=None, foreign_key="modifiers.id", primary_key=True)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "employee_id": "123e4567-e89b-12d3-a456-426614174000",
                "modifier_id": "123e4567-e89b-12d3-a456-426614174001",
            }
        }
    )


class PlayerLabInvestmentLink(SQLModel, table=True):
    """Link table for players and lab investments."""

    __tablename__ = "player_lab_investment_link"

    player_id: str | None = Field(default=None, foreign_key="players.id", primary_key=True)
    lab_id: str | None = Field(default=None, foreign_key="labs.id", primary_key=True)
    part: float = Field(default=0.0, ge=0.0, le=1.0, description="The part of the lab that the player owns.")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "player_id": "123e4567-e89b-12d3-a456-426614174000",
                "lab_id": "123e4567-e89b-12d3-a456-426614174001",
                "part": 0.5,
            }
        }
    )
