from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.logger import init_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    from src.background.scheduler import bg_scheduler
    bg_scheduler.start()
    # await init_db()
    yield
    bg_scheduler.shutdown()