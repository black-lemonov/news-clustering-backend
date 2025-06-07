from typing import Optional
from contextlib import asynccontextmanager

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

import asyncio


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"
    
    url: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    published_at: Mapped[str]
    content: Mapped[str]
    cluster_id: Mapped[int | None] = mapped_column(
        ForeignKey("cluster.id")
    )
    cluster: Mapped[Optional["Cluster"]] = relationship(
        back_populates="news"
    )
    summary: Mapped[Optional["Summary"]] = relationship(
        back_populates="news"
    )
    
    
class Cluster(Base):
    __tablename__ = "cluster"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[str] = mapped_column(default=datetime.now().isoformat())
    news_url: Mapped[str] = mapped_column(
        ForeignKey("news.url")
    )
    news: Mapped[Optional["News"]] = relationship(
        back_populates="cluster"
    )

    
class Summary(Base):
    __tablename__ = "summary"
    
    news_url: Mapped[str] = mapped_column(
        ForeignKey("news.url"), primary_key=True
    )
    content: Mapped[str]
    positive_rates: Mapped[int] = mapped_column(default=0)
    negative_rates: Mapped[int] = mapped_column(default=0)
    
    news: Mapped[Optional["News"]] = relationship(
        back_populates="summary"
    )
    

engine = create_async_engine("sqlite+aiosqlite:///news.db")
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with session_factory() as session:
        yield session

    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        

@asynccontextmanager
async def session_scope(): 
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(init_db())