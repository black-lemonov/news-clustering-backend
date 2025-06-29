from typing import Annotated

from fastapi import APIRouter, status, Path

from src.dependencies import SessionDep
from src.enums.rating import RateType, RateAction
from src.services.rating_service import update_summary_rate


ratings_router = APIRouter(prefix="/summaries", tags=["Оценки"])


@ratings_router.patch(
    "/{cluster_n}/{rate_type}/{action}",
    summary="Обновить рейтинг реферата",
    status_code=status.HTTP_200_OK
)
async def update_summary_rate_endpoint(
        cluster_n: Annotated[int, Path(description="Номер кластера")],
        rate_type: Annotated[RateType, Path(description="Тип оценки", examples=["like", "dislike"])],
        action: Annotated[RateAction, Path(description="Тип действия с оценкой", examples=["add", "remove"])],
        session: SessionDep,
) -> str:
    await update_summary_rate(
        session,
        cluster_n,
        rate_type,
        action
    )

    return "Оценка успешна установлена"