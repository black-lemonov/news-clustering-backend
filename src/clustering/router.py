from fastapi import APIRouter

from src.clustering.service import clustering_task

clustering_router = APIRouter(
    prefix="/clustering"
)

@clustering_router.get(
    ""
)
async def start_clustering():
    await clustering_task()
    return "Кластеризация выполнена"
