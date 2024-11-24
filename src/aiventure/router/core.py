"""Core routes for the API."""

import random
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from aiventure import __version__
from aiventure.models import Health, Version


router = APIRouter()


@router.get("/health", response_model=Health)
async def health() -> Health:
    """Health endpoint for the API."""
    return Health(status="healthy")


@router.get("/version", response_model=Version)
async def version() -> Version:
    """Version endpoint for the API."""
    return Version(version=__version__)


@router.get("/avatars", response_model=list[str])
async def avatars() -> list[str]:
    """Get all avatar images."""
    list_images = list(Path("public/avatars").glob("*.png"))
    random.shuffle(list_images)

    return [image.as_posix() for image in list_images]


@router.get("/avatars/{avatar}", response_class=FileResponse)
async def avatar(avatar: str) -> FileResponse:
    """Get an avatar image."""
    return FileResponse(f"public/avatars/{avatar}")
