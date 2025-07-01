from src.clustering.deps import get_clustering_model
from src.clustering.service import make_clusters
from src.database import session_scope
from src.deps import get_logger
from src.parsers.deps import get_parsers
from src.parsers.service import run_parsers


async def parsing_job():
    logger = get_logger()
    parsers = get_parsers(logger)
    await run_parsers(parsers)


async def clustering_job():
    alg = get_clustering_model()
    logger = get_logger()
    async with session_scope() as session:
        await make_clusters(session, alg, logger)
