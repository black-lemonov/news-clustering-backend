import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_logger():
    return logging.getLogger("app")
