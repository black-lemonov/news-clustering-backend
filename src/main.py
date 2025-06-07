from typing import Annotated

import math
from fastapi import FastAPI, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from contextlib import asynccontextmanager

import uvicorn

from background_task import start_background_task
from database import get_session, News, Summary, init_db

from schemas import SummaryScheme, SummaryWithSourcesScheme, SourceScheme, SummarySchemeWithPagination, Pagination


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await init_db()
    # asyncio.create_task(
    #     start_background_task()
    # ) 
    yield
    

app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get(
    "/summaries",
    tags=["Рефераты ✒️"],
    summary="Получить список всех рефератов"
)
async def get_all_summaries(
    page: Annotated[int, Query(ge=0)],
    size: Annotated[int, Query(ge=1)],
    session: SessionDep
) -> SummarySchemeWithPagination:
    offset_min = page * size
    offset_max = (page + 1) * size
    
    query = (
        select(
            News.title,
            Summary.content,
            News.published_at,
            News.cluster_n
        )
        .join(Summary.news)
    )
    all_news_w_summary = await session.execute(query)
    all_news_w_summary = all_news_w_summary.all()
    
    return SummarySchemeWithPagination(
        data=[
            SummaryScheme(
                title=row.title, 
                summary=row.content, 
                created_at=row.published_at,
                cluster_n=row.cluster_n
            )
            for row in all_news_w_summary[offset_min:offset_max]
        ],
        pagination=Pagination(
            page=page,
            size=size,
            total=math.ceil(len(all_news_w_summary) / size) - 1,
        )
    )


@app.get(
    "/summaries/{id}",
    tags=["Рефераты ✒️"],
    summary="Получить реферат по id с источниками"
)
async def get_news_in_cluster_by_id(id: int, session: SessionDep) -> SummaryWithSourcesScheme:
    query = (
        select(News.url, News.title)
        .where(News.cluster_n == id)
    )
    sources = await session.execute(query)
    
    query = (
        select(
            News.title,
            Summary.content,
            News.published_at,
        )
        .join(Summary.news)
        .where(News.cluster_n == id)
    )
    summaries = await session.execute(query)
    summary = summaries.first()
    return SummaryWithSourcesScheme(
        title=summary.title,
        summary=summary.content,
        created_at=summary.published_at,
        cluster_n=id,
        news=[
            SourceScheme(
                url=row.url,
                title=row.title
            )
            for row in sources.all()
        ]
    )
    

@app.patch(
    "/cluster/{id}/like/add",
    tags=["Оценки"],
    summary="Поставить 👍 реферату"
)
async def add_like_to_summary(id: int, session: SessionDep):
    subquery = (
        select(News.url)
        .where(News.cluster_n == id)
        .scalar_subquery()
    )
    query = (
        select(Summary)
        .where(Summary.news_url.in_(subquery))
    )
    summary = await session.execute(query)
    summary = summary.scalars().first()
    summary.positive_rates += 1
    await session.commit()
    
    return {"ok": True, "msg": "Успех"}


@app.patch(
    "/cluster/{id}/like/remove",
    tags=["Оценки"],
    summary="Убрать 👍 у реферата"
)
async def remove_like_from_summary(id: int, session: SessionDep):
    subquery = (
        select(News.url)
        .where(News.cluster_n == id)
        .scalar_subquery()
    )
    query = (
        select(Summary)
        .where(Summary.news_url.in_(subquery))
    )
    summary = await session.execute(query)
    summary = summary.scalars().first()
    if summary.positive_rates > 0:
        summary.positive_rates -= 1
    await session.commit()
    
    return {"ok": True, "msg": "Успех"}

    

@app.patch(
    "/cluster/{id}/dislike/add",
    tags=["Оценки"],
    summary="Поставить 👎 реферату"
)
async def add_dislike_to_summary(id: int, session: SessionDep):
    subquery = (
        select(News.url)
        .where(News.cluster_n == id)
        .scalar_subquery()
    )
    query = (
        select(Summary)
        .where(Summary.news_url.in_(subquery))
    )
    summary = await session.execute(query)
    summary = summary.scalars().first()
    summary.negative_rates += 1
    await session.commit()
    
    return {"ok": True, "msg": "Успех"}



@app.patch(
    "/cluster/{id}/dislike/remove",
    tags=["Оценки"],
    summary="Убрать 👎 у реферата"
)
async def remove_dislike_from_summary(id: int, session: SessionDep):
    subquery = (
        select(News.url)
        .where(News.cluster_n == id)
        .scalar_subquery()
    )
    query = (
        select(Summary)
        .where(Summary.news_url.in_(subquery))
    )
    summary = await session.execute(query)
    summary = summary.scalars().first()
    if summary.negative_rates > 0:
        summary.negative_rates -= 1
    await session.commit()
    
    return {"ok": True, "msg": "Успех"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    
