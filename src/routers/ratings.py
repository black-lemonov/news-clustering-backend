from fastapi import APIRouter

from src.dependencies import SessionDep
from src.schemas.rating import RateType, RateAction
from src.services.rating_service import update_summary_rate


ratings_router = APIRouter(prefix="/summaries", tags=["Оценки"])


@ratings_router.patch("/{cluster_n}/{rate_type}/{action}", summary="Обновить рейтинг реферата")
async def update_summary_rate_endpoint(
        cluster_n: int,
        rate_type: RateType,
        action: RateAction,
        session: SessionDep
):
    await update_summary_rate(
        session,
        cluster_n,
        rate_type,
        action
    )

    return {"status": "OK", "message": "Оценка добавлена"}