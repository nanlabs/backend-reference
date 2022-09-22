
import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.config import ApiSettings, Settings
from routes.routers import api_router

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

API_SETTINGS: ApiSettings = Settings.get_api_settings()

app = FastAPI(
    title=API_SETTINGS.title,
    debug=API_SETTINGS.debug,
    version=API_SETTINGS.version
)

# Add routes
app.include_router(api_router)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_SETTINGS.allow_origins,
    allow_credentials=API_SETTINGS.allow_credentials,
    allow_methods=API_SETTINGS.allow_methods,
    allow_headers=API_SETTINGS.allow_headers,
)


@app.middleware('http')
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration * 100) + " ms"
    return response


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=API_SETTINGS.host,
        port=API_SETTINGS.port,
        debug=API_SETTINGS.debug,
        reload=True,
        reload_includes=["*"]
    )
