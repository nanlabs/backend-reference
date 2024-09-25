from fastapi import APIRouter

from .base_routes import router as base_routes
from .note_routes import router as note_router

router = APIRouter()

router.include_router(base_routes, prefix="", tags=["base"])
router.include_router(note_router, prefix="/notes", tags=["notes"])
