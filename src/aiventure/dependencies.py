"""Dependencies for the API."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, WebSocket
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from aiventure.config import settings
from aiventure.db import UsersCRUD
from aiventure.game_manager import game_manager
from aiventure.models import UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan for the API."""
    async_engine = create_async_engine(settings.db_connection_str, future=True)

    app.state.async_engine = async_engine
    app.state.async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    await init_database(app.state.async_session())
    game_task = asyncio.create_task(game_manager.start(app.state.async_session()))

    yield

    await game_manager.stop()
    await game_task
    await app.state.async_engine.dispose()


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
    async with UsersCRUD(session) as crud:
        try:
            await crud.create(UserCreate(email="test@test.com", password="test"))
        except IntegrityError:
            await crud.rollback()
            await crud.get_by_email(email="test@test.com")
