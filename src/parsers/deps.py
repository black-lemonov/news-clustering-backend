from src.parsers.news_parser import NewsParser
from src.parsers.parsers_factories import JSONParsersFactory


def get_parsers() -> list[NewsParser]:
    parsers = JSONParsersFactory().load_parsers()
    return parsers