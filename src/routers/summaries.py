from typing import Annotated

from fastapi import APIRouter, status, Path

from src.dependencies import SessionDep, PaginationDep
from src.responses.summaries_list_w_pagination import SummariesListWithPagination
from src.responses.summary_w_sources import SummaryWithSources
from src.services.news_service import get_news_sources_by_cluster
from src.services.summaries_service import get_paginated_summaries, get_summary_by_cluster

summaries_router = APIRouter(prefix="/summaries", tags=["Рефераты ✒️"])


@summaries_router.get(
    "",
    summary="Получить список всех рефератов",
    status_code=status.HTTP_200_OK
)
async def get_all_summaries(
    pagination: PaginationDep,
    session: SessionDep
) -> SummariesListWithPagination:
    summaries = await get_paginated_summaries(session, pagination.page, pagination.size)
    return SummariesListWithPagination.from_summaries(
        summaries=summaries, page=pagination.page, size=pagination.size
    )


@summaries_router.get(
    "/{cluster_n}",
    summary="Получить реферат по id с источниками",
    status_code=status.HTTP_200_OK
)
async def get_summary_w_sources_by_id(
    cluster_n: Annotated[int, Path(description="Номер кластера")],
    session: SessionDep
) -> SummaryWithSources:
    summary = await get_summary_by_cluster(session, cluster_n)
    sources = await get_news_sources_by_cluster(session, cluster_n)

    return SummaryWithSources.from_summary_w_list(
        summary, sources=sources
    )
