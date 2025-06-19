from sklearn.cluster import DBSCAN
from sklearn.pipeline import Pipeline, make_pipeline
from src.text_processing.tfidf_vectorizer import StemmedTfidfVectorizer
from src.config import MAX_DF, MIN_DF, EPS, MIN_SAMPLES


vectorizer = (
    StemmedTfidfVectorizer(
        max_df=MAX_DF,
        min_df=MIN_DF,
        decode_error="ignore"
    )
)

algorithm = DBSCAN(
    eps=EPS,
    min_samples=MIN_SAMPLES
)

clustering_pipeline: Pipeline = make_pipeline(
    vectorizer,
    algorithm
)