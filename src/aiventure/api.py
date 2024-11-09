"""Entrypoint for the API."""

from fastapi import FastAPI

from aiventure import __version__
from aiventure.dependencies import lifespan
from aiventure.router.core import router as core_router
from aiventure.router.v1.endpoints import api_router


app = FastAPI(
    title="AI Venture API",
    version=__version__,
    description="Backend server for AI Venture",
    lifespan=lifespan,
)

app.include_router(core_router, prefix="")
app.include_router(api_router, prefix="/api/v1")
