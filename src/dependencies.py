import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PARSERS
from src.database import get_session
from src.text_processing.news_parser import NewsParser

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_logger():
    return logging.getLogger("app")


def get_parsers():
    parsers = [
        NewsParser(**config)
        for config in PARSERS
    ]
    return parsers
