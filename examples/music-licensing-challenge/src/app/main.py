from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router

app = FastAPI(
    title="Music Licensing API",
    description="API for managing music licensing workflow",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Music Licensing API"}
