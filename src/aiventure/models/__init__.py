"""Models for the database and API."""

# NOTE: We export all the table models so they are available to the ORM.
from .ai_model import (
    AI_MODEL_TYPE_MAPPING,
    AIModel,
    AIModelBase,
    AIModelType,
    AIModelTypeBase,
    AIModelTypeEnum,
)
from .core import (
    Health,
    StatusMessage,
    UUIDModel,
    Version,
)
from .employee import Employee, EmployeeBase
from .lab import Lab, LabBase
from .links import EmployeeModifierLink
from .location import LOCATION_MAPPING, Location, LocationBase, LocationEnum
from .modifier import (
    MODIFIER_MAPPING,
    MODIFIER_TYPE_MAPPING,
    Modifier,
    ModifierBase,
    ModifierEnum,
    ModifierType,
    ModifierTypeBase,
    ModifierTypeEnum,
)
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
from .user import (
    Token,
    TokenData,
    User,
    UserAdminPatch,
    UserBase,
    UserCreate,
    UserPatch,
    UserRead,
)


__all__ = [
    # AI Model
    "AI_MODEL_TYPE_MAPPING",
    "AIModel",
    "AIModelBase",
    "AIModelType",
    "AIModelTypeBase",
    "AIModelTypeEnum",
    # Core
    "Health",
    "StatusMessage",
    "UUIDModel",
    "Version",
    # Employee
    "Employee",
    "EmployeeBase",
    # Lab
    "Lab",
    "LabBase",
    # Links
    "EmployeeModifierLink",
    # Location
    "LOCATION_MAPPING",
    "Location",
    "LocationBase",
    "LocationEnum",
    # Modifier
    "MODIFIER_MAPPING",
    "MODIFIER_TYPE_MAPPING",
    "Modifier",
    "ModifierBase",
    "ModifierEnum",
    "ModifierType",
    "ModifierTypeBase",
    "ModifierTypeEnum",
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
    # User
    "Token",
    "TokenData",
    "User",
    "UserAdminPatch",
    "UserBase",
    "UserCreate",
    "UserPatch",
    "UserRead",
]
