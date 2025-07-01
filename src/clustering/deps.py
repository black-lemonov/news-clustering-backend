from typing import Annotated

from fastapi import Depends
from sklearn.cluster import DBSCAN
from sklearn.pipeline import Pipeline, make_pipeline

from src.clustering.config import MAX_DF, MIN_DF, EPS, MIN_SAMPLES
from src.clustering.preprocessing.tfidf_vectorizer import StemmedTfidfVectorizer


def get_clustering_model() -> Pipeline:
    vectorizer = StemmedTfidfVectorizer(
        max_df=MAX_DF, min_df=MIN_DF, decode_error="ignore"
    )
    algorithm = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
    return make_pipeline(vectorizer, algorithm)


ClusteringDep = Annotated[Pipeline, Depends(get_clustering_model)]
