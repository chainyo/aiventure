"""Dependencies for the API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from aiventure.config import settings
from aiventure.db import QualityCRUD, RoleCategoryCRUD, RoleCRUD
from aiventure.models import QUALITY_MAPPING, ROLE_CATEGORY_MAPPING, ROLE_MAPPING


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan for the API."""
    async_engine = create_async_engine(settings.db_connection_str, echo=True, future=True)

    app.state.async_engine = async_engine
    _session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    app.state.async_session = _session

    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    await init_database(app.state.async_session())
    yield


async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Get an async session."""

    async with request.app.state.async_session() as session:
        yield session


async def init_database(session: AsyncSession) -> None:
    """Initialize the database."""
    quality_crud = QualityCRUD(session)
    for quality in QUALITY_MAPPING.values():
        await _try_create_or_update(quality_crud, quality)

    role_category_crud = RoleCategoryCRUD(session)
    for role_category in ROLE_CATEGORY_MAPPING.values():
        await _try_create_or_update(role_category_crud, role_category)

    role_crud = RoleCRUD(session)
    for role in ROLE_MAPPING.values():
        await _try_create_or_update(role_crud, role)


async def _try_create_or_update(crud: BaseModel, model: BaseModel) -> None:
    """Try to create or update a model."""
    try:
        await crud.create(model)
    except IntegrityError:
        await crud.update(model)
