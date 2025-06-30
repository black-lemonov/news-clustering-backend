from typing import Annotated
from fastapi import (
    APIRouter,
    File,
    UploadFile,
    status,
    Query,
    HTTPException,
)

from src.exceptions import BaseError
from src.parsers.service import add_new_parser, move_site_to_selected, remove_site_from_selected
from src.parsers.utils import (
    get_available_parsers_sites_urls,
    get_config_from_fastapi_file,
    load_parser_config_example,
    load_last_parsing_time_from_config,
    get_selected_parsers_sites_urls,
)

parsers_router = APIRouter(
    prefix="/parsers",
    tags=["Парсеры 🤖"],
    # dependencies=[AuthDep]
)


@parsers_router.post(
    "/",
    summary="Загрузить JSON-файл с конфигурацией парсера",
    status_code=status.HTTP_201_CREATED,
)
def load_parser(
    parser_config: Annotated[
        UploadFile, File(description="JSON файл с конфигурацией парсера")
    ],
) -> str:
    try:
        parser_config = get_config_from_fastapi_file(parser_config)
        add_new_parser(parser_config)
        return "Парсер успешно добавлен"
    except BaseError as be:
        raise HTTPException(status_code=be.code, detail=be.msg)


@parsers_router.get(
    "/sites/selected",
    summary="Получить список выбранных сайтов для парсинга",
    status_code=status.HTTP_200_OK,
)
def get_selected_sites() -> list[str]:
    return get_selected_parsers_sites_urls()


@parsers_router.get(
    "/sites/available",
    summary="Получить список доступных сайтов для парсинга",
    status_code=status.HTTP_200_OK,
)
def get_available_sites() -> list[str]:
    return get_available_parsers_sites_urls()


@parsers_router.patch(
    "/sites",
    summary="Добавить новостной сайт в парсинг",
    status_code=status.HTTP_200_OK
)
def add_site(
    site_url: Annotated[str, Query(description="URL главной страницы")],
) -> str:
    try:
        move_site_to_selected(site_url)
        return "Сайт внесен в список"
    except BaseError as be:
        raise HTTPException(status_code=be.code, detail=be.msg)


@parsers_router.delete(
    "/sites",
    summary="Убрать новостной сайт из парсинга",
    status_code=status.HTTP_200_OK,
)
def remove_site(
    site_url: Annotated[str, Query(description="URL главной страницы")],
) -> str:
    try:
        remove_site_from_selected(site_url)
        return "Сайт убран из парсинга"
    except BaseError as be:
        raise HTTPException(status_code=be.code, detail=be.msg)


@parsers_router.get(
    "/template",
    summary="Получить шаблон файла конфигурации",
    status_code=status.HTTP_200_OK,
)
def get_parser_template() -> dict:
    return load_parser_config_example()


@parsers_router.get(
    "/timestamp",
    summary="Получить дату последнего парсинга",
    status_code=status.HTTP_200_OK,
)
async def get_last_parsing_time() -> str:
    return load_last_parsing_time_from_config()
