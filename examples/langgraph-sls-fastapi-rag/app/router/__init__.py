from fastapi import APIRouter

from app.index_graph.router import router as index_router
from app.rag_graph.router import router as rag_router

from .base_routes import router as base_routes

router = APIRouter()

router.include_router(base_routes, prefix="", tags=["base"])
router.include_router(index_router, prefix="/index", tags=["index"])
router.include_router(rag_router, prefix="/retrieve", tags=["rag"])
