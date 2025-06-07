from typing import Annotated, Optional

from fastapi import FastAPI, Depends
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import asyncio

import uvicorn

engine = create_async_engine("sqlite+aiosqlite:///news.db")

news_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with news_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"
    
    url: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    published_at: Mapped[datetime]
    content: Mapped[str]
    cluster_id: Mapped[int | None] = mapped_column(ForeignKey("cluster.id"))
    summary: Mapped[Optional["Summary"]] = relationship(back_populates="news")
    cluster: Mapped[Optional["Cluster"]] = relationship(back_populates="news")
    
    
class Summary(Base):
    __tablename__ = "summary"
    
    news_url: Mapped[str] = mapped_column(ForeignKey("news.url"), primary_key=True)
    content: Mapped[str]
    positive_rates: Mapped[int] = 0
    negative_rates: Mapped[int] = 0
    news: Mapped["News"] = relationship(back_populates="summary")
    

class Cluster(Base):
    __tablename__ = "cluster"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = datetime.now()
    news: Mapped["News"] = relationship(back_populates="cluster")

    
    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get(
    "/news",
    tags=["Новости"],
    summary="Получить список новостей",
)
def get_news(session: SessionDep):
    return {}


@app.get(
    "/cluster/{id}",
    tags=["Кластеры"],
    summary="Получить новости из кластера по id",
)
def get_cluster_by_id(id: int):
    return {}


@app.put(
    "/cluster/{id}",
    tags=["Кластеры"],
    summary="Оценить пересказ",
)
def rate_summary(id: int, rate: int):
    return {}


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run("main:app", reload=True)
