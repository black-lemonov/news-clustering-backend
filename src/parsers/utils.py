import json

from fastapi import UploadFile

from src.exceptions import WrongFormatError


def get_config_from_fastapi_file(upload_file: UploadFile) -> dict:
    if upload_file.content_type != "application/json":
        raise WrongFormatError("Файл должен иметь формат json")
        
    return json.load(upload_file.file)


def get_selected_parsers_sites_urls() -> list[str]:
    with open("application.json") as f:
        conf = json.load(f)
        return conf["selected_sites_urls"]
    

def get_available_parsers_sites_urls() -> list[str]:
    with open("application.json") as f:
        conf = json.load(f)
        return [p["site_url"] for p in conf["parsers_configs"]]
    

def load_parser_config_example() -> dict:
    with open("parser_config.json") as f:
        return json.load(f)


def load_last_parsing_time_from_config() -> str:
    with open("application.json") as f:
        return json.load(f)["last_parsing_time"]
    