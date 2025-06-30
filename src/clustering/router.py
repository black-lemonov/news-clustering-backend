from fastapi import APIRouter, status

from src.clustering.deps import ClusteringDep
from src.clustering.service import make_clusters
from src.deps import LoggerDep, SessionDep

clustering_router = APIRouter(
    prefix="/clustering",
    tags=["Кластеризация 👥"],
    # dependencies=[AuthDep]
)

@clustering_router.get(
    "/run",
    summary="Запустить алгоритм кластеризации",
    status_code=status.HTTP_200_OK
)
async def start_clustering_in_bg(
        clustering_alg: ClusteringDep,
        session: SessionDep,
        logger: LoggerDep,
) -> str:
    try:
        await make_clusters(session, clustering_alg, logger)
        return "Кластеризация выполнена"
    except Exception as e:
        logger.error("Ошибка при кластеризации: %s", e)
