from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from contextlib import asynccontextmanager

import uvicorn

from background_task import start_background_task
from database import get_session, News, Summary


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
    tags=["Реферат"],
    summary="Получить список всех рефератов"
)
async def get_all_news(session: SessionDep):
    query = select(News)
    all_news = await session.execute(query)
    return all_news.scalars().all()


@app.get(
    "/cluster/{id}",
    tags=["Кластер"],
    summary="Получить новости из кластера по id"
)
async def get_news_in_cluster_by_id(id: int, session: SessionDep):
    query = select(News).where(News.cluster_n == id)
    news_in_cluster = await session.execute(query)
    return {
        "news": news_in_cluster.scalars().all()
    }


@app.get(
    "/cluster/{id}/summary",
    tags=["Реферат"],
    summary="Получить реферат для кластера"
)
async def get_cluster_summary_by_id(id: int, session: SessionDep):
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
    return summary.scalars().first()
    

@app.patch(
    "/cluster/{id}/like/add",
    tags=["Оценка"],
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
    
    return {"message": "Success"}


@app.patch(
    "/cluster/{id}/like/remove",
    tags=["Оценка"],
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
    
    return {"message": "Success"}
    

@app.patch(
    "/cluster/{id}/dislike/add",
    tags=["Оценка"],
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
    
    return {"message": "Success"}


@app.patch(
    "/cluster/{id}/dislike/remove",
    tags=["Оценка"],
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
    
    return {"message": "Success"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    
