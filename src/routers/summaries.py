import math
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException

from src.dependencies import SessionDep
from src.dto.base import Pagination
from src.dto.summaries import SummarySchemeWithPagination, SummaryScheme, SummaryWithSourcesScheme
from src.services.summary_service import get_paginated_summaries, get_summary_with_sources


summaries_router = APIRouter(prefix="/summaries", tags=["Рефераты ✒️"])


@summaries_router.get("", summary="Получить список всех рефератов")
async def get_all_summaries(
        page: Annotated[int, Query(ge=0)],
        size: Annotated[int, Query(ge=1)],
        session: SessionDep
) -> SummarySchemeWithPagination:
    summaries, total_count = await get_paginated_summaries(session, page, size)

    return SummarySchemeWithPagination(
        data=[
            SummaryScheme(
                title=row.title,
                summary=row.content,
                created_at=row.published_at,
                cluster_n=row.cluster_n
            )
            for row in summaries
        ],
        pagination=Pagination(
            page=page,
            size=size,
            total=math.ceil(total_count / size) if size > 0 else 0,
        )
    )


@summaries_router.get("/{cluster_n}", summary="Получить реферат по id с источниками")
async def get_summary_w_sources_by_id(
        cluster_n: int,
        session: SessionDep
) -> SummaryWithSourcesScheme:


    return {"status": "OK", "message": "Оценка добавлена"}