from logging import Logger
from sklearn.pipeline import Pipeline
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.news.service import get_all_news_urls, get_news_content_by_urls, set_cluster_n


async def make_clusters(
    session: AsyncSession, clustering_alg: Pipeline, logger: Logger
) -> None:
    news_urls = await get_all_news_urls(session)
    news_content = await get_news_content_by_urls(session, news_urls)
    clusters_labels = clustering_alg.fit_predict(news_content)
    logger.debug("Получено %d кластеров", len(set(clusters_labels)))
    for label, url in zip(clusters_labels, news_urls):
        label = int(label)
        await set_cluster_n(session, url, label)
