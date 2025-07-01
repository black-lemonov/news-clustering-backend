from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import init_db
from src.logger import init_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    await init_db()
    yield
