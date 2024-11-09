"""Dependencies for the API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from aiventure.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan for the API."""
    async_engine = create_async_engine(settings.db_connection_str, echo=True, future=True)

    app.state.async_engine = async_engine
    _session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    app.state.async_session = _session

    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    yield


async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Get an async session."""

    async with request.app.state.async_session() as session:
        yield session
