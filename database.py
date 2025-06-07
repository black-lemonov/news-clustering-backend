from typing import Optional
from contextlib import asynccontextmanager

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

import asyncio

from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass

class News(Base):
    __tablename__ = "news"
    
    url: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    content: Mapped[str]
    
    cluster_id: Mapped[int | None] = mapped_column(
        ForeignKey("cluster.id", ondelete="SET NULL")
    )
    cluster: Mapped[Optional["Cluster"]] = relationship(
        back_populates="news_items",
        cascade="save-update, merge"
    )
    
    summary: Mapped[Optional["Summary"]] = relationship(
        back_populates="news",
        uselist=False,
        cascade="all, delete-orphan"
    )

class Cluster(Base):
    __tablename__ = "cluster"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Опционально: ссылка на главную новость
    main_news_url: Mapped[Optional[str]] = mapped_column(
        ForeignKey("news.url", ondelete="SET NULL")
    )
    
    # Отношение ко всем новостям кластера
    news_items: Mapped[list["News"]] = relationship(
        back_populates="cluster",
        cascade="save-update, merge, expunge"
    )

class Summary(Base):
    __tablename__ = "summary"
    
    news_url: Mapped[str] = mapped_column(
        ForeignKey("news.url", ondelete="CASCADE"), 
        primary_key=True
    )
    content: Mapped[str]
    positive_rates: Mapped[int] = mapped_column(default=0)
    negative_rates: Mapped[int] = mapped_column(default=0)
    
    news: Mapped["News"] = relationship(
        back_populates="summary",
        single_parent=True
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
