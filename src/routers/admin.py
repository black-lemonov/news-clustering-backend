import json
import secrets

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.params import Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse

from src.config import SUMM_MODELS_FILEPATHS, ADMIN_USERNAME, ADMIN_PASSWORD
from src.dependencies import SessionDep
from src.parsers.parsers_selection import get_parsers_sites_urls, remove_parser, add_new_parser
from src.services.bg_service import get_last_parsing_time_from_config, start_bg_task
from src.services.summaries_service import create_summary_for_news
from src.summarizers.utils.model_selection import set_model_by_name, get_selected_model_name


def verify_admin(credentials: HTTPBasicCredentials = Security(HTTPBasic())):
    username_correct = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    password_correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


admin_router = APIRouter(
    prefix="/admin",
    tags=["Управление 🤖"],
    dependencies=[Depends(verify_admin)]
)


@admin_router.post("/summaries/", summary="Сгенерировать реферат для новости")
async def generate_summary(news_url: str, session: SessionDep):
    await create_summary_for_news(session, news_url)
    return {"status": "OK", "message": "Реферат создан"}


@admin_router.get("/models", summary="Получить список доступных моделей")
def get_available_models():
    return {"available_models": list(SUMM_MODELS_FILEPATHS.keys())}


@admin_router.get("/models/selected", summary="Получить название выбранной модели")
def get_selected_model():
    name = get_selected_model_name()
    return {"selected_model": name}


@admin_router.post("/models/selected", summary="Выбрать модель")
def set_model(model_name: str):
    set_model_by_name(model_name)
    return {"status": "OK", "message": "Модель успешно установлена"}


@admin_router.get("/parsers/sites", summary="Получить список новостных сайтов для парсинга")
def get_all_parsers():
    return {"sites_urls": get_parsers_sites_urls()}


@admin_router.delete("/parsers/sites", summary="Удалить новостной сайт из парсинга")
def delete_parser(site_url: str):
    remove_parser(site_url)
    return {"status": "OK", "message": "Парсер удален"}


@admin_router.post("/parsers", summary="Загрузить JSON-файл с конфигурацией парсера")
def load_parser(file: UploadFile):
    parser_config = json.load(file.file)
    add_new_parser(parser_config)
    return {"status": "OK", "message": "Парсер добавлен"}


@admin_router.get("/parsers/template", summary="Получить шаблон файла конфигурации")
def get_parser_template():
    return JSONResponse(
        {
            "site_url": "",
            "article_selector": "",
            "title_selector": "",
            "url_selector": "",
            "date_selector": "",
            "content_selector": "",
            "stop_words": []
        }
    )

@admin_router.get("/system", summary="Запустить парсинг и алгоритм кластеризации")
async def start_bg_task_():
    await start_bg_task()
    return {"status": "OK", "message": "Алгоритм парсинга запущен"}


@admin_router.get("/system/timestamp", summary="Получить дату последнего парсинга")
async def get_last_parsing_time():
    last_time = get_last_parsing_time_from_config()
    return {"last_parsing_time": last_time}
