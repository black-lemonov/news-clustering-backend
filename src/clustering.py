from datetime import datetime

from sqlalchemy import select, or_, func
import asyncio
from sklearn.cluster import DBSCAN

from database import session_scope, News
from config import MAX_DF, MIN_DF, EPS, MIN_SAMPLES, CLUSTER_TTL
from tfidf_vectorizer import StemmedTfidfVectorizer


async def run_clustering():
    async with session_scope() as session:
        query = (
            select(News)
        )
        
        all_news = (
            await session.execute(query)
        )
        
        vectorizer = StemmedTfidfVectorizer(
            max_df=MAX_DF,
            min_df=MIN_DF,
            decode_error="ignore"
        )
        
        all_news = all_news.scalars().all()
        
        vectors = vectorizer.fit_transform(
            [row.content for row in all_news]
        )

        dbscan = DBSCAN(
            eps=EPS,
            min_samples=MIN_SAMPLES
        )
        
        clusters_labels = dbscan.fit_predict(vectors)
        
        for label, news in zip(clusters_labels, all_news):
            news.cluster_n = int(label)

if __name__ == "__main__":
    asyncio.run(run_clustering())