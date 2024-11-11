"""Router for the web interface."""

from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/", response_class=FileResponse)
async def main() -> FileResponse:
    """Return the main page."""
    return FileResponse("public/index.html")


@router.get("/login")
async def login() -> FileResponse:
    """Return the login page."""
    return FileResponse("public/login.html")


@router.get("/play")
async def play() -> FileResponse:
    """Return the play page."""
    return FileResponse("public/play.html")


@router.get("/register")
async def register() -> FileResponse:
    """Return the register page."""
    return FileResponse("public/register.html")
