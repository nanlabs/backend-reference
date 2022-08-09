from fastapi import APIRouter

from controllers import users_controller

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(users_controller.router, tags=["Users"], prefix="/users")
