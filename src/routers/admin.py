from fastapi import APIRouter

from src.config import SELECTED_MODEL, SUMM_MODELS_FILEPATHS
from src.dependencies import SessionDep
from src.services.news_service import del_cluster_in_news, del_news_by_cluster

admin_router = APIRouter(prefix="/admin", tags=["Управление 🤖"])


@admin_router.delete("/{cluster_n}", summary="Удалить кластер")
async def del_cluster(
        cluster_n: int,
        session: SessionDep
) -> dict:
    await del_cluster_in_news(session, cluster_n)

    return {"status": "OK", "message": "Кластер удален"}

@admin_router.post("/summaries/{cluster_n}", summary="Создать новый реферат для кластера")
async def generate_new_summary(
        cluster_n: int,
        session: SessionDep
) -> dict:
    await del_cluster_in_news(session, cluster_n)

    return {"status": "OK", "message": "Кластер удален"}


@admin_router.delete("/news/{cluster_n}", summary="Удалить кластер и все новости")
async def del_cluster_w_news(
        cluster_n: int,
        session: SessionDep
) -> dict:
    await del_news_by_cluster(session, cluster_n)

    return {"status": "OK", "message": "Кластер и новости удалены"}


@admin_router.get("/models", summary="Получить список доступных моделей")
def get_available_models() -> dict:
    return {"available_models": SUMM_MODELS_FILEPATHS.keys()}


@admin_router.get("/models/selected", summary="Получить название выбранной модели")
def get_selected_model() -> dict:
    return {"selected_model": SELECTED_MODEL}


@admin_router.post("/models/selected", summary="Выбрать модель")
def set_model(model_name: str) -> dict:
    if SUMM_MODELS_FILEPATHS.get(model_name):
       SELECTED_MODEL = model_name
       return {"status": "OK", "message": "Модель успешно установлена"}

    return {"status": "ERROR", "message": "Такой модели не существует"}
