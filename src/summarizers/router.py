from typing import Annotated

from fastapi import APIRouter, status, Query

from src.deps import AuthDep
from src.summarizers.schemas import AvailableModelsList, SelectedModelName
from src.summarizers.service import set_model_by_name


summarizers_router = APIRouter(
    prefix="/summarizers",
    tags=["Модели для реферирования 👾"],
    dependencies=[AuthDep]
)


@summarizers_router.get(
    "",
    summary="Получить список доступных моделей",
    status_code=status.HTTP_200_OK
)
def get_available_models() -> AvailableModelsList:
    return AvailableModelsList()


@summarizers_router.get(
    "/selected",
    summary="Получить название выбранной модели",
    status_code=status.HTTP_200_OK
)
def get_selected_model() -> SelectedModelName:
    return SelectedModelName()


@summarizers_router.patch(
    "/selected",
    summary="Выбрать модель",
    status_code=status.HTTP_200_OK
)
def set_model(
        model_name: Annotated[str, Query(description="Название модели")]
) -> str:
    set_model_by_name(model_name)
    return "Модель успешно установлена"