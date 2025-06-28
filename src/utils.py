import json


def load_parser_config_example() -> dict:
    with open("parser_config.json") as f:
        return json.load(f)


def load_last_parsing_time_from_config() -> str:
    with open("application.json") as f:
        return json.load(f)["last_parsing_time"]


def load_news_csv_table_headers_from_config() -> list[str]:
    with open("application.json") as f:
        return json.load(f)["news_csv_table_columns"]
