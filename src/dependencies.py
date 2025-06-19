import logging
from logging import Logger
from typing import Annotated

from fastapi import Depends
from sklearn.cluster import DBSCAN
from sklearn.pipeline import Pipeline, make_pipeline
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PARSERS, MAX_DF, MIN_DF, EPS, MIN_SAMPLES
from src.database import get_session
from src.parsers.news_parser import NewsParser
from src.summarizers.base_summarizer import BaseSummarizer
from src.summarizers.tr_summarizer import TRSummarizer
from src.preprocessing.tfidf_vectorizer import StemmedTfidfVectorizer

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_logger() -> Logger:
    return logging.getLogger("app")


def get_parsers() -> list[NewsParser]:
    parsers = [
        NewsParser(**config)
        for config in PARSERS
    ]
    return parsers

def get_clustering_model() -> Pipeline:
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
    return make_pipeline(
        vectorizer, algorithm
    )


def get_summarizer() -> BaseSummarizer:
    return TRSummarizer()
