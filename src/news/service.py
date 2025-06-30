import csv
from datetime import datetime
from io import StringIO

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import News
from src.news.utils import load_news_csv_table_headers_from_config
from src.summaries.schemas import Source


async def get_all_news_urls(session: AsyncSession) -> list[str]:
    result = await session.execute(
        select(News.url)
    )
    return list(result.scalars().all())


async def get_news_content_by_urls(session: AsyncSession, urls: list[str]) -> list[str]:
    result = await session.execute(
        select(News.content)
        .where(News.url.in_(urls))
    )
    return list(result.scalars().all())


async def set_cluster_n(
        session: AsyncSession,
        news_url: str,
        cluster_n: int
) -> None:
    await session.execute(
        update(News)
        .where(News.url == news_url)
        .values(cluster_n=cluster_n)
    )
    await session.commit()


def add_news(
        session: AsyncSession,
        url: str,
        title: str,
        published_at: datetime,
        content: str
) -> None:
    session.add(
        News(
            url=url,
            title=title,
            published_at=published_at,
            content=content
        )
    )


async def del_cluster_in_news(session: AsyncSession, cluster_n: int) -> None:
    await session.execute(
        update(News)
        .where(News.cluster_n == cluster_n)
        .values(cluster_n=None)
    )


async def del_news_by_cluster(session: AsyncSession, cluster_n: int) -> None:
    await session.execute(
        delete(News).where(News.cluster_n == cluster_n)
    )


async def get_news_w_summaries(session: AsyncSession) -> list[list]:
    news_items = await session.execute(
        select(News)
        .options(selectinload(News.summary))
        .where(News.summary.any())
    )
    return [
        [
            n.url,
            n.title,
            n.published_at.isoformat(),
            n.content,
            n.summary[0].content,
            n.summary[0].positive_rates,
            n.summary[0].negative_rates
        ]
        for n in news_items.scalars().all()
    ]


async def get_news_sources_by_cluster(session: AsyncSession, cluster_n: int) -> list[Source]:
    sources = await session.execute(
        select(News.url, News.title)
        .where(News.cluster_n == cluster_n)
    )

    return [
        Source(url=s.url, title=s.title)
        for s in sources.scalars().all()
    ]

async def generate_csv_table_for_news(session: AsyncSession) -> str:
    news_w_summaries = await session.execute(
        select(News)
        .options(selectinload(News.summary))
        .where(News.summary.any())
    )

    if not news_w_summaries:
        raise HTTPException(status_code=404, detail="Нет новостей с рефератами")

    output = StringIO()
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    headers = load_news_csv_table_headers_from_config()

    writer.writerow(headers)

    for n in news_w_summaries.all():
        writer.writerow(
            (
                n.url,
                n.title,
                n.published_at.isoformat(),
                n.content,
                n.summary[0].content,
                n.summary[0].positive_rates,
                n.summary[0].negative_rates
            )
        )

    output.seek(0)

    return output.getvalue()