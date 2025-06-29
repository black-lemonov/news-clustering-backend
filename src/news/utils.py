import json


def load_news_csv_table_headers_from_config() -> list[str]:
    with open("application.json") as f:
        return json.load(f)["news_csv_table_columns"]
