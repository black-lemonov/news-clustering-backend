import asyncio
from contextlib import asynccontextmanager

import nltk
from fastapi import FastAPI

from src.logger import init_logger
from src.text_processing.start import start_background_task
from src.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    nltk.download("stopwords")
    init_logger()
    await init_db()
    asyncio.create_task(start_background_task())
    yield