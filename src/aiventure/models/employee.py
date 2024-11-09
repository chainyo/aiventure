"""Employees models."""

from sqlmodel import Field
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel


class EmployeeBase(UUIDModel):
    """Employee model."""

    name: str
    salary: int
    image_url: str
    role_id: int = Field(foreign_key="roles.id")
    quality_id: int = Field(foreign_key="qualities.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "bonuses": ["Free lunch", "Free gym"],
                "salary": 100000,
                "image_url": "https://example.com/image.png",
                "role_id": 1,
                "quality_id": 1,
            }
        }
    )

class Employee(EmployeeBase, table=True):
    """Table for employees."""

    __tablename__ = "employees"
