from pydantic import BaseModel, Field

from src.config import SUMM_MODELS_FILEPATHS


class AvailableModelsList(BaseModel):
    available_models: list[str] = Field(default_factory=lambda: list(SUMM_MODELS_FILEPATHS.keys()))
