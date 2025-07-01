import asyncio
import json
from datetime import datetime

from src.exceptions import AlreadyExistsError, NotFoundError
from src.parsers.news_parser import NewsParser
from src.parsers.utils import (
    get_available_parsers_sites_urls,
    get_selected_parsers_sites_urls,
)


def add_new_parser(parser_config: dict) -> None:
    available_sites = get_available_parsers_sites_urls()
    if parser_config["site_url"] in available_sites:
        raise AlreadyExistsError("Конфигурация для сайта с таким URL уже загружена")

    with open("application.json") as f:
        conf = json.load(f)
        conf["parsers_configs"].append(parser_config)
        conf["selected_sites_urls"].append(parser_config["site_url"])

    with open("application.json", "w") as f:
        json.dump(conf, f)


def move_site_to_selected(site_url: str) -> None:
    available_sites = get_available_parsers_sites_urls()
    if site_url not in available_sites:
        raise NotFoundError("Сайт с таким URL не найден в списке доступных парсеров")

    with open("application.json") as f:
        conf = json.load(f)
        if site_url in conf["selected_sites_urls"]:
            raise AlreadyExistsError("Сайт уже парсится")
        conf["selected_sites_urls"].append(site_url)

    with open("application.json", "w") as f:
        json.dump(conf, f)


def remove_site_from_selected(site_url: str) -> None:
    selected_sites = get_selected_parsers_sites_urls()
    if site_url not in selected_sites:
        raise NotFoundError("Сайт с таким URL не найден в списке парсеров")
    with open("application.json") as f:
        conf = json.load(f)
        if site_url in conf["selected_sites_urls"]:
            conf["selected_sites_urls"].remove(site_url)

    with open("application.json", "w") as f:
        json.dump(conf, f)


async def run_parsers(parsers: list[NewsParser]) -> None:
    await asyncio.gather(*[p.parse() for p in parsers])


def update_timer():
    with open("application.json") as f:
        conf = json.load(f)
        conf["last_parsing_time"] = datetime.now().isoformat()

    with open("application.json", "w") as f:
        json.dump(conf, f)
