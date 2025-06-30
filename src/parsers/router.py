from typing import Annotated
from fastapi import (
    APIRouter,
    File,
    UploadFile,
    status,
    Query,
    BackgroundTasks,
    HTTPException,
)

from src.exceptions import WrongFormatError
from src.parsers.deps import ParsersDep
from src.parsers.service import add_new_parser, remove_parser, run_parsers, update_timer
from src.parsers.utils import (
    get_config_from_fastapi_file,
    load_parser_config_example,
    load_last_parsing_time_from_config,
    get_parsers_sites_urls,
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
    except WrongFormatError as e:
        raise HTTPException(status_code=e.code, detail=e.msg)


@parsers_router.get(
    "/sites",
    summary="Получить список новостных сайтов для парсинга",
    status_code=status.HTTP_200_OK,
)
def get_all_parsers() -> list[str]:
    return get_parsers_sites_urls()


@parsers_router.delete(
    "/sites",
    summary="Удалить новостной сайт из парсинга",
    status_code=status.HTTP_200_OK,
)
def delete_parser(
    site_url: Annotated[str, Query(description="URL главной страницы")],
) -> str:
    remove_parser(site_url)
    return "Парсер успешно удален"


@parsers_router.get(
    "/template",
    summary="Получить шаблон файла конфигурации",
    status_code=status.HTTP_200_OK,
)
def get_parser_template() -> dict:
    return load_parser_config_example()


@parsers_router.get(
    "/run", summary="Запустить парсинг", status_code=status.HTTP_202_ACCEPTED
)
async def start_parsers(parsers: ParsersDep, bg_tasks: BackgroundTasks) -> str:
    await run_parsers(parsers)
    bg_tasks.add_task(update_timer)
    return "Парсеры успешно запущены"


@parsers_router.get(
    "/timestamp",
    summary="Получить дату последнего парсинга",
    status_code=status.HTTP_200_OK,
)
async def get_last_parsing_time() -> str:
    return load_last_parsing_time_from_config()
