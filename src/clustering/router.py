from fastapi import APIRouter, status, BackgroundTasks

from src.clustering.deps import ClusteringDep
from src.clustering.service import make_clusters
from src.deps import AuthDep, SessionDep

clustering_router = APIRouter(
    prefix="/clustering",
    tags=["Кластеризация 👥"],
    dependencies=[AuthDep]
)

@clustering_router.get(
    "/run",
    summary="Запустить алгоритм кластеризации",
    status_code=status.HTTP_202_ACCEPTED
)
async def start_clustering_in_bg(
        clustering_alg: ClusteringDep,
        session: SessionDep,
        bg_tasks: BackgroundTasks
) -> str:
    bg_tasks.add_task(
        make_clusters,
    session,
        clustering_alg
    )
    return "Кластеризация запущена"
