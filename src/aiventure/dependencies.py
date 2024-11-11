"""Dependencies for the API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, WebSocket
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from aiventure.config import settings
from aiventure.db import (
    AIModelTypeCRUD,
    BaseCRUD,
    LocationCRUD,
    ModifierTypeCRUD,
    QualityCRUD,
    RoleCategoryCRUD,
    RoleCRUD,
    UsersCRUD,
)
from aiventure.models import (
    AI_MODEL_TYPE_MAPPING,
    LOCATION_MAPPING,
    MODIFIER_TYPE_MAPPING,
    QUALITY_MAPPING,
    ROLE_CATEGORY_MAPPING,
    ROLE_MAPPING,
    UserCreate,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan for the API."""
    async_engine = create_async_engine(settings.db_connection_str, echo=True, future=True)

    app.state.async_engine = async_engine
    app.state.async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    await init_database(app.state.async_session())
    yield


async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Get an async session."""

    async with request.app.state.async_session() as session:
        yield session


async def get_async_session_from_websocket(websocket: WebSocket) -> AsyncGenerator[AsyncSession, None]:
    """Get an async session from a websocket."""
    async with websocket.scope["app"].state.async_session() as session:
        yield session


async def init_database(session: AsyncSession) -> None:
    """Initialize the database."""
    ai_model_type_crud = AIModelTypeCRUD(session)
    for ai_model_type in AI_MODEL_TYPE_MAPPING.values():
        await _try_create_or_update(ai_model_type_crud, ai_model_type)

    location_crud = LocationCRUD(session)
    for location in LOCATION_MAPPING.values():
        await _try_create_or_update(location_crud, location)

    quality_crud = QualityCRUD(session)
    for quality in QUALITY_MAPPING.values():
        await _try_create_or_update(quality_crud, quality)

    modifier_type_crud = ModifierTypeCRUD(session)
    for modifier_type in MODIFIER_TYPE_MAPPING.values():
        await _try_create_or_update(modifier_type_crud, modifier_type)

    role_category_crud = RoleCategoryCRUD(session)
    for role_category in ROLE_CATEGORY_MAPPING.values():
        await _try_create_or_update(role_category_crud, role_category)

    role_crud = RoleCRUD(session)
    for role in ROLE_MAPPING.values():
        await _try_create_or_update(role_crud, role)

    users_crud = UsersCRUD(session)
    await _try_create_or_update(users_crud, UserCreate(email="test@test.com", password="test"))


async def _try_create_or_update(crud: BaseCRUD, model: BaseModel) -> None:
    """Try to create or update a model."""
    try:
        await crud.create(model)
    except IntegrityError:
        await crud.update(model)
