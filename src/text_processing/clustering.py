import asyncio

from src.dependencies import get_logger
from src.database import session_scope
from src.services.news_service import get_all_news_urls, get_news_content_by_urls, set_cluster_n
from src.services.summary_service import add_summary, check_if_summary_exist
from src.text_processing.clustering_pipeline import clustering_pipeline
from src.text_processing.summarization import summarize

logger = get_logger()


async def run_clustering():
    logger.info("Запуск кластеризации...")
    async with session_scope() as session:
        news_urls = await get_all_news_urls(session)
        logger.debug("Считаны новости из БД")
        
        news_content = await get_news_content_by_urls(session, news_urls)
        
        clusters_labels = clustering_pipeline.fit_predict(news_content)
        logger.debug(f"Кластеризация выполнена: {len(set(clusters_labels))} кластеров")
        have_summary = set()
        for label, url, content in zip(clusters_labels, news_urls, news_content):
            label = int(label)
            await set_cluster_n(session, url, label)
            

            if label in have_summary:
                continue
            
            if not (await check_if_summary_exist(session, url)):
                add_summary(
                    session,
                    url,
                    content
                )
                
            have_summary.add(label)

        logger.info("Записи в БД обновлены")
        

if __name__ == "__main__":
    asyncio.run(run_clustering())