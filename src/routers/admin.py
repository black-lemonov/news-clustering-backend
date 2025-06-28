import json

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import Response, JSONResponse

from src.dependencies import SessionDep, AuthDep
from src.dto.available_models_list import AvailableModelsList
from src.dto.last_parsing_time import LastParsingTime
from src.dto.news_csv_table import NewsCSVTable
from src.dto.parsers_sites_urls import ParsersSitesUrls
from src.dto.selected_model_name import SelectedModelName
from src.services.parsers_service import remove_parser, add_new_parser
from src.services.bg_service import start_bg_task
from src.services.news_service import del_news_by_cluster, generate_csv_table_for_news
from src.services.summaries_service import create_summary_for_news
from src.summarizers.utils.model_selection import set_model_by_name
from src.utils import load_parser_config_example


admin_router = APIRouter(
    prefix="/admin",
    tags=["Управление 🤖"],
    dependencies=[AuthDep]
)


@admin_router.post(
    "/summaries",
    summary="Сгенерировать реферат для новости",
    status_code=status.HTTP_201_CREATED
)
async def generate_summary(news_url: str, session: SessionDep) -> Response:
    await create_summary_for_news(session, news_url)
    return Response(content="Реферат сгенерирован")


@admin_router.get(
    "/models",
    summary="Получить список доступных моделей",
    status_code=status.HTTP_200_OK
)
def get_available_models() -> AvailableModelsList:
    return AvailableModelsList()


@admin_router.get(
    "/models/selected",
    summary="Получить название выбранной модели",
    status_code=status.HTTP_200_OK
)
def get_selected_model() -> SelectedModelName:
    return SelectedModelName()


@admin_router.post(
    "/models/selected",
    summary="Выбрать модель",
    status_code=status.HTTP_200_OK
)
def set_model(model_name: str) -> Response:
    set_model_by_name(model_name)
    return Response(content="Модель успешно установлена")


@admin_router.get(
    "/parsers/sites",
    summary="Получить список новостных сайтов для парсинга",
    status_code=status.HTTP_200_OK
)
def get_all_parsers() -> ParsersSitesUrls:
    return ParsersSitesUrls()


@admin_router.delete(
    "/parsers/sites",
    summary="Удалить новостной сайт из парсинга",
    status_code=status.HTTP_200_OK
)
def delete_parser(site_url: str) -> Response:
    remove_parser(site_url)
    return Response(content="Парсер успешно удален")


@admin_router.post(
    "/parsers",
    summary="Загрузить JSON-файл с конфигурацией парсера",
    status_code=status.HTTP_201_CREATED
)
def load_parser(file: UploadFile) -> Response:
    parser_config = json.load(file.file)
    add_new_parser(parser_config)
    return Response(content="Парсер успешно добавлен")


@admin_router.get(
    "/parsers/template",
    summary="Получить шаблон файла конфигурации",
    status_code=status.HTTP_200_OK
)
def get_parser_template() -> JSONResponse:
    return JSONResponse(load_parser_config_example())


@admin_router.get(
    "/system",
    summary="Запустить парсинг и алгоритм кластеризации",
    status_code=status.HTTP_202_ACCEPTED
)
async def start_bg_task_() -> Response:
    await start_bg_task()
    return Response(content="Алгоритм успешно запущен")


@admin_router.get(
    "/system/timestamp",
    summary="Получить дату последнего парсинга",
    status_code=status.HTTP_200_OK
)
async def get_last_parsing_time() -> LastParsingTime:
    return LastParsingTime()


@admin_router.delete(
    "/clusters/{cluster_n}",
    summary="Удалить кластер",
    status_code=status.HTTP_200_OK
)
async def delete_cluster(cluster_n: int, session: SessionDep) -> Response:
    await del_news_by_cluster(session, cluster_n)
    return Response(content="Кластер новостей был успешно удален")


@admin_router.get(
    "/clusters/export",
    summary="Скачать таблицу .csv",
    status_code=status.HTTP_200_OK
)
async def export_news_with_summaries(session: SessionDep) -> NewsCSVTable:
    news_csv_table = await generate_csv_table_for_news(session)
    return NewsCSVTable(content=news_csv_table)
