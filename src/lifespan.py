from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.logger import init_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    yield
