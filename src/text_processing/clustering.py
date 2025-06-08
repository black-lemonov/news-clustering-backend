import asyncio
from sklearn.cluster import DBSCAN

from src.models.summary import Summary
from src.dependencies import get_logger
from src.database import session_scope
from src.config import MAX_DF, MIN_DF, EPS, MIN_SAMPLES
from src.services.news_service import get_all_news_urls, get_news_content_by_urls, set_cluster_n
from src.text_processing.tfidf_vectorizer import StemmedTfidfVectorizer
from src.text_processing.summarization import summarize

logger = get_logger()


async def run_clustering():
    logger.info("Запуск кластеризации...")
    async with session_scope() as session:
        news_urls = await get_all_news_urls(session)
        logger.debug("Считаны новости из БД")
        
        vectorizer = StemmedTfidfVectorizer(
            max_df=MAX_DF,
            min_df=MIN_DF,
            decode_error="ignore"
        )

        news_content = await get_news_content_by_urls(session, news_urls)
        vectors = vectorizer.fit_transform(news_content)
        
        logger.debug("Векторизован текст")

        dbscan = DBSCAN(
            eps=EPS,
            min_samples=MIN_SAMPLES
        )
        
        clusters_labels = dbscan.fit_predict(vectors)
        logger.debug(f"Кластеризация выполнена: {len(clusters_labels)} кластеров")
        have_summary = set()
        for label, url, content in zip(clusters_labels, news_urls, news_content):
            label = int(label)
            await set_cluster_n(session, url, label)

            if label in have_summary:
                continue
            
            session.add(
                Summary(
                    news_url=url,
                    content=summarize(content)
                )
            )
            have_summary.add(label)
        
        logger.info("Записи в БД обновлены")
        
            

if __name__ == "__main__":
    asyncio.run(run_clustering())