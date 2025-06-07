from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from contextlib import asynccontextmanager

import uvicorn

from config import PARSING_INTERVAL
from background_task import start_background_task
from database import get_session, News


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(
        start_background_task(PARSING_INTERVAL)
    ) 
    yield
    

app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get(
    "/news",
    tags=["Новости"],
    summary="Получить список новостей",
)
async def get_news(session: SessionDep):
    query = select(News)
    result = await session.execute(query)
    return result.scalars().all()


@app.get(
    "/cluster/{id}",
    tags=["Кластеры"],
    summary="Получить новости из кластера по id",
)
async def get_cluster_by_id(id: int, session: SessionDep):
    query = select(News).where(News.cluster_n == id)
    result = await session.execute(query)
    return result.scalars().all()


@app.put(
    "/cluster/{id}",
    tags=["Рефераты"],
    summary="Оценить пересказ",
)
def rate_summary(id: int, rate: int):
    return {}


if __name__ == "__main__":
    # asyncio.run(init_db())
    uvicorn.run("main:app", reload=True)
    
