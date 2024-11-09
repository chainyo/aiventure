"""Regroup all the database CRUD operations."""

from .base import BaseCRUD
from .quality import QualityCRUD
from .role import RoleCategoryCRUD, RoleCRUD


__all__ = ["BaseCRUD", "QualityCRUD", "RoleCategoryCRUD", "RoleCRUD"]
