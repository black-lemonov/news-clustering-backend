import asyncio
from src.bg.config import CLUSTERING_TASK_NAME, PARSING_TASK_NAME
from src.clustering.service import make_clusters
from src.parsers.service import start_parsing
from src.bg.celery import app, logger


@app.task(name=PARSING_TASK_NAME)
def parsing_task():
    asyncio.run(start_parsing(logger))


@app.task(name=CLUSTERING_TASK_NAME)
def clustering_task():
    asyncio.run(make_clusters(logger))
