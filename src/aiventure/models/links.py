"""Links tables for many-to-many relationships."""

from sqlmodel import Field, SQLModel


class EmployeeModifierLink(SQLModel, table=True):
    """Link table for employees and modifiers."""

    __tablename__ = "employee_modifier_link"

    employee_id: str | None = Field(default=None, foreign_key="employees.id", primary_key=True)
    modifier_id: str | None = Field(default=None, foreign_key="modifiers.id", primary_key=True)
