"""Entrypoint for the API."""

from fastapi import FastAPI

from aiventure import __version__
from aiventure.dependencies import lifespan
from aiventure.router.authentication import router as auth_router
from aiventure.router.core import router as core_router
from aiventure.router.game import router as game_router


app = FastAPI(
    title="AI Venture API",
    version=__version__,
    description="Backend server for AI Venture",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(core_router, prefix="", tags=["core"])
app.include_router(game_router, prefix="/api/game", tags=["game"])
