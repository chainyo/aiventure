"""User entity models."""

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel


class UserBase(SQLModel):
    """Users table"""

    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    is_admin: bool = Field(default=False)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "password": "password",
                "is_admin": False,
            }
        }
    )


class User(UserBase, UUIDModel, table=True):
    """User model"""

    __tablename__ = "users"


class UserRead(UUIDModel):
    """User read model"""

    email: str
    is_admin: bool

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "test@example.com",
                "is_admin": False,
            }
        }
    )


class UserCreate(UserBase):
    """User create model"""

    email: str
    password: str

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "password": "password",
            }
        }
    )


class UserPatch(BaseModel):
    """User patch model"""

    email: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
            }
        }
    )


class UserAdminPatch(BaseModel):
    """User admin patch model"""

    email: str
    is_admin: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "is_admin": True,
            }
        }
    )


class Token(BaseModel):
    """Token model"""

    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "token",
                "token_type": "bearer",
            }
        }
    )


class TokenData(BaseModel):
    """TokenData model"""

    username: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "test@example.com",
            }
        }
    )
