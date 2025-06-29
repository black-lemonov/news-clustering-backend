import json

from src.summarizers.config import SUMM_MODELS_FILEPATHS


def get_available_models_names() -> list[str]:
    return list(SUMM_MODELS_FILEPATHS.keys())


def get_selected_model_name() -> str:
    with open("application.json") as f:
        summ_config = json.load(f)
        return summ_config["selected_model"]
