from datetime import datetime

from sklearn.cluster import DBSCAN
from sqlalchemy import select, or_, func
import asyncio

from database import session_scope, News
from config import MAX_DF, MIN_DF, EPS, MIN_SAMPLES, CLUSTER_TTL
from tfidf_vectorizer import StemmedTfidfVectorizer


async def run_clustering():
    
    async with session_scope() as session:
        print("ЧТО")
        actual_news_by_clusters = select(
            News.cluster_n,
            News.published_at
        ).group_by(
            News.cluster_n
        ).having(
            func.datediff(
                func.current_date(), 
                func.min(News.published_at)
            ) > CLUSTER_TTL
        )
        print("ЧТО")
        res = await session.execute(
            actual_news_by_clusters
        )
        print(res)
        print("Я не прав?")
        
        # subquery_result = (
        #     await session.execute(subquery)
        # ).scalars().unique().all() 
        
        # query = select(News).where(
        #     or_(
        #         News.cluster_id.is_(None),
        #         News.cluster_id.in_(subquery_result)
        #     )
        # )
        
        # result = await session.execute(query)
        # news = result.scalars().all()

        # vectorizer = StemmedTfidfVectorizer(
        #     max_df=MAX_DF,
        #     min_df=MIN_DF,
        #     decode_error="ignore"
        # )
        # vectors = vectorizer.fit_transform(
        #     [row.content for row in news]
        # )

        # dbscan = DBSCAN(
        #     eps=EPS,
        #     min_samples=MIN_SAMPLES
        # )
        
        # dbscan_index_2_db_index = {}
        # db_index = len(subquery_result)
        # for news_row, dbscan_index in zip(news, dbscan.fit_predict(vectors)):
        #     if dbscan_index not in dbscan_index_2_db_index:
        #         dbscan_index_2_db_index[dbscan_index] = db_index
        #         db_index += 1
        #     news_row.cluster_id = dbscan_index_2_db_index[dbscan_index]
            
        # await session.commit()
        
        # min_dates_subquery = (
        #     select(
        #         News.cluster_id,
        #         func.min(News.published_at).label('min_published')
        #     )
        #     .group_by(News.cluster_id)
        #     .alias('min_dates')
        # )
        
        # random_urls_subquery = (
        #     select(
        #         News.cluster_id,
        #         News.url.label('random_url')
        #     )
        #     .distinct(News.cluster_id)
        #     .order_by(News.cluster_id, func.random())
        #     .alias('random_urls')
        # )
        
        # query = (
        #     select(
        #         min_dates_subquery.c.cluster_id,
        #         random_urls_subquery.c.random_url,
        #         min_dates_subquery.c.min_published
        #     )
        #     .select_from(min_dates_subquery)
        #     .join(
        #         random_urls_subquery,
        #         min_dates_subquery.c.cluster_id == random_urls_subquery.c.cluster_id
        #     )
        # )
        
        # result = (await session.execute(query)).scalars().all()
        
        # for row in result:
        #     session.add(
        #         Cluster(
        #             id=row.cluster_id,
        #             created_at=row.min_published,
        #             news_url=row.random_url
        #         )
        #     )


if __name__ == "__main__":
    asyncio.run(run_clustering())