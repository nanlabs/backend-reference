from time import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.config import settings
from app.router import router as api_router

app = FastAPI(title=settings.app.title, version=settings.app.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_time_elapsed(request: Request, call_next) -> Response:  # type: ignore
    start_time = time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time() - start_time)
    return response


app.include_router(api_router)

handler = Mangum(app)
