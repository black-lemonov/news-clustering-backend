from fastapi import APIRouter, status
from fastapi.responses import Response

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
        cluster_n: int,
        rate_type: RateType,
        action: RateAction,
        session: SessionDep,
) -> Response:
    await update_summary_rate(
        session,
        cluster_n,
        rate_type,
        action
    )

    return Response(content="Оценка успешна установлена")