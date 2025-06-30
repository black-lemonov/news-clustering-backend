import logging
import secrets
from logging import Logger
from typing import Annotated

from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import ADMIN_USERNAME, ADMIN_PASSWORD
from src.database import get_session
from src.pagination import Pagination


SessionDep = Annotated[AsyncSession, Depends(get_session)]
PaginationDep = Annotated[Pagination, Depends(Pagination)]


def get_logger() -> Logger:
    return logging.getLogger("app")


LoggerDep = Annotated[Logger, get_logger]


def verify_admin(credentials: HTTPBasicCredentials = Security(HTTPBasic())):
    try:
        username_correct = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
        password_correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка авторизации: некоторые поля отсутствуют"
        )

    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

    return credentials.username


AuthDep = Depends(verify_admin)
