import json
from abc import ABC, abstractmethod
from logging import Logger

from src.parsers.news_parser import NewsParser


class ParsersFactory(ABC):
    @abstractmethod
    def load_parsers(self, logger: Logger | None = None) -> list[NewsParser]:
        ...


class JSONParsersFactory(ParsersFactory):
    def load_parsers(self, logger: Logger | None = None) -> list[NewsParser]:
        with open("application.json") as conf_file:
            conf_dict = json.load(conf_file)
            parsers = [
                NewsParser(**conf)
                for conf in conf_dict["parsers_configs"]
                if conf["site_url"] in conf_dict["selected_sites_urls"]
            ]
            if logger:
                for p in parsers:
                    p.set_logger(logger)
            return parsers
