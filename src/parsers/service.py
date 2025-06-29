import asyncio
import json
from datetime import datetime

from src.deps import get_logger
from src.parsers.deps import get_parsers


def add_new_parser(parser_config: dict) -> None:
    logger = get_logger()
    logger.debug(parser_config)
    with open("application.json") as f:
        conf = json.load(f)
        conf["parsers_configs"].append(parser_config)
        conf["selected_sites_urls"].append(parser_config["site_url"])

    with open("application.json", "w") as f:
        json.dump(conf, f)


def remove_parser(site_url: str) -> None:
    with open("application.json") as f:
        conf = json.load(f)
        if site_url in conf["selected_sites_urls"]:
            conf["selected_sites_urls"].remove(site_url)

    with open("application.json", 'w') as f:
        json.dump(conf, f)
        

async def run_parsers() -> None:
    await asyncio.gather(
        *[p.parse() for p in get_parsers()]
    )


def update_timer():
    with open("application.json") as f:
        conf = json.load(f)
        conf["last_parsing_time"] = datetime.now().isoformat()

    with open("application.json", 'w') as f:
        json.dump(conf, f)
