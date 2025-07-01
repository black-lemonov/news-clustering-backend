from logging import Logger

from src.clustering.deps import get_clustering_model
from src.database import session_scope
from src.news.service import get_all_news_urls, get_news_content_by_urls, set_cluster_n


async def make_clusters(logger: Logger) -> None:
    async with session_scope() as session:
        news_urls = await get_all_news_urls(session)
        news_content = await get_news_content_by_urls(session, news_urls)
        clusters_labels = get_clustering_model().fit_predict(news_content)
        logger.debug("Получено %d кластеров", len(set(clusters_labels)))
        for label, url in zip(clusters_labels, news_urls):
            label = int(label)
            await set_cluster_n(session, url, label)
        logger.debug("Кластеризация завершена")
