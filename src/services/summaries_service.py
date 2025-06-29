from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_summarizer
from src.dto.source import Source
from src.dto.summary import SummaryDTO
from src.models.news import News
from src.models.summary import Summary
from src.services.news_service import get_news_content_by_urls


async def get_cluster_news_urls(session: AsyncSession, cluster_n: int) -> list[str]:
    result = await session.execute(
        select(News.url)
        .where(News.cluster_n == cluster_n)
    )
    return list(result.scalars().all())


async def get_cluster_summary(session: AsyncSession, cluster_n: int) -> Summary | None:
    news_urls = await get_cluster_news_urls(session, cluster_n)
    if not news_urls:
        return None
    result = await session.execute(
        select(Summary)
        .where(Summary.news_url.in_(news_urls))
    )
    return result.scalars().first()


async def get_paginated_summaries(
    session: AsyncSession,
    page: int,
    size: int
) -> list[SummaryDTO]:
    offset = page * size
    query = (
        select(
            News.title,
            Summary.content,
            News.published_at,
            News.cluster_n
        )
        .join(Summary.news)
        .where(News.cluster_n.is_not(None))
        .order_by(desc(News.published_at))
        .offset(offset)
        .limit(size)
    )
    result = await session.execute(query)
    summaries = result.all()

    return [
        SummaryDTO(
            title=s.title,
            content=s.content,
            created_at=s.published_at,
            cluster_n=s.cluster_n
        )
        for s in summaries
    ]


async def get_summary_by_cluster(session: AsyncSession, cluster_n: int) -> SummaryDTO:

    summary = await session.execute(
        select(News.title, Summary.content, News.published_at, News.cluster_n)
        .join(Summary.news)
        .where(News.cluster_n == cluster_n)
        .limit(1)
    )
    summary = summary.scalars().first()

    return SummaryDTO(
        title=summary.title,
        content=summary.content,
        created_at=summary.published_at,
        cluster_n=summary.cluster_n
    )


async def get_summary_w_sources(session: AsyncSession, cluster_n: int) -> tuple | None:
    sources_query = select(News.url, News.title).where(News.cluster_n == cluster_n)
    sources_result = await session.execute(sources_query)

    summary_query = (
        select(News.title, Summary.content, News.published_at)
        .join(Summary.news)
        .where(News.cluster_n == cluster_n)
        .limit(1)
    )
    summary_result = await session.execute(summary_query)
    summary = summary_result.first()

    if not summary:
        return None

    return summary, [
        Source(url=row.url, title=row.title)
        for row in sources_result.all()
    ]


async def check_if_summary_exist(session: AsyncSession, news_url: str) -> bool:
    query = (
        select(Summary)
        .where(Summary.news_url == news_url)
    )
    summary = (await session.execute(query)).first()

    return summary is not None


def add_summary(session: AsyncSession, news_url: str, summary: str) -> None:
    summary = Summary(
        news_url=news_url,
        content=summary
    )
    session.add(summary)


async def create_summary_for_news(session: AsyncSession, news_url: str):
    content = (await get_news_content_by_urls(session, [news_url]))[0]

    summarizer = get_summarizer()
    summary = summarizer.summarize(content)

    summary = Summary(
        news_url=news_url,
        content=summary
    )
    session.add(summary)
    