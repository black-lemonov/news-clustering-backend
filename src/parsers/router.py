import json
from typing import Annotated
from fastapi import APIRouter, File, UploadFile, status, Query
from fastapi.responses import JSONResponse

from src.const import URL_REGEX
from src.deps import AuthDep
from src.parsers.schemas import LastParsingTime, ParsersSitesUrls
from src.parsers.service import add_new_parser, remove_parser, run_parsers, update_timer
from src.parsers.utils import load_parser_config_example


parsers_router = APIRouter(
    prefix="/parsers",
    tags=["Парсеры 🤖"],
    dependencies=[AuthDep]
)


@parsers_router.post(
    "/",
    summary="Загрузить JSON-файл с конфигурацией парсера",
    status_code=status.HTTP_201_CREATED
)
def load_parser(
        parser_config: Annotated[UploadFile, File(description="JSON файл с конфигурацией парсера")]
) -> str:
    parser_config = json.load(parser_config.file)
    add_new_parser(parser_config)
    return "Парсер успешно добавлен"


@parsers_router.get(
    "/sites",
    summary="Получить список новостных сайтов для парсинга",
    status_code=status.HTTP_200_OK
)
def get_all_parsers() -> ParsersSitesUrls:
    return ParsersSitesUrls()


@parsers_router.delete(
    "/sites",
    summary="Удалить новостной сайт из парсинга",
    status_code=status.HTTP_200_OK
)
def delete_parser(
        site_url: Annotated[str, Query(description="URL главной страницы", regex=URL_REGEX)]
) -> str:
    remove_parser(site_url)
    return "Парсер успешно удален"


@parsers_router.get(
    "/template",
    summary="Получить шаблон файла конфигурации",
    status_code=status.HTTP_200_OK
)
def get_parser_template() -> JSONResponse:
    return JSONResponse(load_parser_config_example())


@parsers_router.get(
    "/run",
    summary="Запустить парсинг",
    status_code=status.HTTP_202_ACCEPTED
)
async def start_parsers() -> str:
    await run_parsers()
    update_timer()
    return "Парсеры успешно запущены"


@parsers_router.get(
    "/timestamp",
    summary="Получить дату последнего парсинга",
    status_code=status.HTTP_200_OK
)
async def get_last_parsing_time() -> LastParsingTime:
    return LastParsingTime()
