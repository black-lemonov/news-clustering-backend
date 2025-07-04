import json

from src.summarizers.config import SUMM_MODELS_FILEPATHS


def set_model_by_name(model_name: str) -> None:
    with open("application.json") as f:
        summ_config = json.load(f)
        if model_name in SUMM_MODELS_FILEPATHS.keys():
            summ_config["selected_model"] = model_name

    with open("application.json", "w") as f:
        json.dump(summ_config, f)
