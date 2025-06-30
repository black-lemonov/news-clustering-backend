from typing import Annotated

from fastapi import APIRouter, status, Path, Query

from src.const import URL_REGEX
from src.deps import PaginationDep, SessionDep, AuthDep
import src.news.service as news_service
from src.summaries.enums import RateType, RateAction
from src.summaries.schemas import SummariesListWithPagination, SummaryWithSources, NewsCSVTable
import src.summaries.service as summary_service


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
    summaries = await summary_service.get_paginated_summaries(session, pagination.page, pagination.size)
    return SummariesListWithPagination.from_summaries(
        summaries=summaries, page=pagination.page, size=pagination.size
    )


@summaries_router.post(
    "",
    summary="Сгенерировать реферат для новости",
    status_code=status.HTTP_201_CREATED
)
async def generate_summary(
        news_url: Annotated[str, Query(
            description="URL новости из бд",
            regex=URL_REGEX
        )],
        session: SessionDep
) -> str:
    await summary_service.create_summary_for_news(session, news_url)
    return "Реферат сгенерирован"


@summaries_router.get(
    "/export",
    summary="Скачать таблицу .csv",
    status_code=status.HTTP_200_OK,
    dependencies=[AuthDep]
)
async def export_news_with_summaries(session: SessionDep) -> NewsCSVTable:
    news_csv_table = await news_service.generate_csv_table_for_news(session)
    return NewsCSVTable(content=news_csv_table)


@summaries_router.get(
    "/{cluster_n}",
    summary="Получить реферат по id с источниками",
    status_code=status.HTTP_200_OK
)
async def get_summary_w_sources_by_id(
    cluster_n: Annotated[int, Path(description="Номер кластера")],
    session: SessionDep
) -> SummaryWithSources:
    summary = await summary_service.get_summary_by_cluster(session, cluster_n)
    sources = await news_service.get_news_sources_by_cluster(session, cluster_n)
    return SummaryWithSources.from_summary_w_list(summary, sources)


@summaries_router.delete(
    "/{cluster_n}",
    summary="Удалить кластер",
    status_code=status.HTTP_200_OK
)
async def delete_cluster(
        cluster_n: Annotated[int, Path(description="Номер кластера")],
        session: SessionDep
) -> str:
    await news_service.del_news_by_cluster(session, cluster_n)
    return "Кластер новостей был успешно удален"


@summaries_router.patch(
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
    await summary_service.update_summary_rate(
        session,
        cluster_n,
        rate_type,
        action
    )
    return "Оценка успешна установлена"