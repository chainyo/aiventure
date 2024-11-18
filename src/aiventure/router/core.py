"""Core routes for the API."""

from fastapi import APIRouter

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
