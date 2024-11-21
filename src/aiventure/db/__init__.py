"""Regroup all the database CRUD operations."""

from .ai_model import AIModelCRUD, AIModelTypeCRUD
from .base import BaseCRUD
from .lab import LabCRUD
from .location import LocationCRUD
from .modifier import ModifierCRUD, ModifierTypeCRUD
from .player import PlayerCRUD
from .quality import QualityCRUD
from .role import RoleCategoryCRUD, RoleCRUD
from .user import UsersCRUD


__all__ = [
    "AIModelCRUD",
    "AIModelTypeCRUD",
    "BaseCRUD",
    "LabCRUD",
    "LocationCRUD",
    "ModifierCRUD",
    "ModifierTypeCRUD",
    "PlayerCRUD",
    "QualityCRUD",
    "RoleCategoryCRUD",
    "RoleCRUD",
    "UsersCRUD",
]
