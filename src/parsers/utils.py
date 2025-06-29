import json


def get_parsers_sites_urls() -> list[str]:
    with open("application.json") as f:
        conf = json.load(f)
        return conf["selected_sites_urls"]
    

def load_parser_config_example() -> dict:
    with open("parser_config.json") as f:
        return json.load(f)


def load_last_parsing_time_from_config() -> str:
    with open("application.json") as f:
        return json.load(f)["last_parsing_time"]
    