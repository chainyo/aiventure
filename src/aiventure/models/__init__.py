"""Models for the database and API."""

# NOTE: We export all the table models so they are available to the ORM.
from .core import (
    Health,
    UUIDModel,
    Version,
)
from .employee import Employee, EmployeeBase
from .quality import QUALITY_MAPPING, Quality, QualityBase, QualityEnum
from .role import (
    ROLE_CATEGORY_MAPPING,
    ROLE_MAPPING,
    Role,
    RoleBase,
    RoleCategory,
    RoleCategoryBase,
    RoleCategoryEnum,
    RoleEnum,
)


__all__ = [
    # Core
    "Health",
    "UUIDModel",
    "Version",
    # Employee
    "Employee",
    "EmployeeBase",
    # Quality
    "QUALITY_MAPPING",
    "Quality",
    "QualityBase",
    "QualityEnum",
    # Role
    "ROLE_CATEGORY_MAPPING",
    "ROLE_MAPPING",
    "Role",
    "RoleBase",
    "RoleCategory",
    "RoleCategoryBase",
    "RoleCategoryEnum",
    "RoleEnum",
]
