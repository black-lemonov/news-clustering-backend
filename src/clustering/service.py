from src.clustering.deps import get_clustering_model
from src.database import session_scope
from src.deps import get_logger
from src.news.service import get_all_news_urls, get_news_content_by_urls, set_cluster_n


async def clustering_task():
    logger = get_logger()
    logger.debug("Запуск кластеризации...")
    async with session_scope() as session:
        news_urls = await get_all_news_urls(session)
        logger.debug("Считаны новости из БД")

        news_content = await get_news_content_by_urls(session, news_urls)

        clusters_labels = get_clustering_model().fit_predict(news_content)
        logger.debug(f"Кластеризация выполнена: {len(set(clusters_labels))} кластеров")
        logger.debug(clusters_labels)

        for label, url, content in zip(clusters_labels, news_urls, news_content):
            label = int(label)
            await set_cluster_n(session, url, label)

        logger.debug("Записи в БД обновлены")