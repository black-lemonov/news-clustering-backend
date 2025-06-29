from fastapi import APIRouter, status

from src.clustering.service import clustering_task
from src.deps import AuthDep

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
async def start_clustering():
    await clustering_task()
    return "Кластеризация выполнена"
