"""Entrypoint for the API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

origins = ["http://localhost:8000", "localhost:8000"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(core_router, prefix="", tags=["core"])
app.include_router(game_router, prefix="/api/game", tags=["game"])

app.mount("/", StaticFiles(directory="public", html=True), name="static")


@app.get("/", response_class=FileResponse)
async def main() -> FileResponse:
    """Return the main page."""
    return FileResponse("public/index.html")
