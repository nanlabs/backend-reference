import uvicorn
from core.config import (
    ALLOWED_CORS_HEADERS,
    ALLOWED_CORS_HOSTS,
    ALLOWED_CORS_METHODS,
    APP_NAME,
    APP_VERSION,
    IS_DEBUG,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routers import api_router


def start_app() -> FastAPI:
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    # Routes
    fast_app.include_router(api_router)

    # Middleware
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_CORS_HOSTS,
        allow_credentials=True,
        allow_methods=ALLOWED_CORS_METHODS,
        allow_headers=ALLOWED_CORS_HEADERS,
    )
    return fast_app


app = start_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
