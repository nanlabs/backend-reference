from fastapi import APIRouter
from .movies import router as movies_router
from .scenes import router as scenes_router
from .graphql import router as graphql_app

router = APIRouter()

router.include_router(movies_router, prefix="/movies", tags=["movies"])
router.include_router(scenes_router, prefix="/movies/scenes", tags=["scenes"])
router.include_router(graphql_app, prefix="/graphql", tags=["graphql"])
