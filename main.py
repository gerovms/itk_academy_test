import sys

from fastapi import FastAPI

from app.api.routers import main_router


try:
    app = FastAPI()
    app.include_router(main_router)
except Exception:
    sys.exit(1)
