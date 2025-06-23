import asyncio

from src.dependencies import get_logger, get_clustering_model, get_summarizer
from src.database import session_scope
from src.config import PARSING_INTERVAL
from src.services.clustering_service import make_clusters
from src.services.news_service import get_all_news_urls, get_news_content_by_urls, set_cluster_n
from src.services.parsers_service import run_parsers
from src.services.summaries_service import add_summary, check_if_summary_exist, generate_summaries_for_clusters

logger = get_logger()


async def start_bg_task():
    while True:
        logger.debug("Запуск парсинга...")
        # await run_parsers()
        logger.debug("Парсинг завершен")

        logger.debug("Запуск кластеризации...")
        async with session_scope() as session:
            news_urls = await get_all_news_urls(session)
            logger.debug("Считаны новости из БД")

            news_content = await get_news_content_by_urls(session, news_urls)

            clusters_labels = get_clustering_model().fit_predict(news_content)
            logger.debug(f"Кластеризация выполнена: {len(set(clusters_labels))} кластеров")
            have_summary = set()
            summarizer = get_summarizer()
            for label, url, content in zip(clusters_labels, news_urls, news_content):
                label = int(label)
                await set_cluster_n(session, url, label)

                if label in have_summary:
                    continue

                if not (await check_if_summary_exist(session, url)):
                    logger.debug("Работает?")
                    try:
                        add_summary(
                            session,
                            url,
                            summarizer.summarize(content)
                        )
                    except Exception as e:
                        logger.error("Ошибка при реферировании")
                        logger.error(e)
                     
                    logger.debug("Работает")

                have_summary.add(label)

            logger.debug("Записи в БД обновлены")

        await asyncio.sleep(PARSING_INTERVAL)


async def start_bg_task2():
    while True:
        # await run_parsers()
        async with session_scope() as session:
            clusters_labels = await make_clusters(session)
            logger.debug(clusters_labels)

            summarizer = get_summarizer()
            await generate_summaries_for_clusters(session, summarizer, clusters_labels)

        await asyncio.sleep(PARSING_INTERVAL)
