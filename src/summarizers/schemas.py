from pydantic import BaseModel, Field

from src.summarizers.utils import get_available_models_names, get_selected_model_name


class AvailableModelsList(BaseModel):
    available_models: list[str] = Field(
        default_factory=get_available_models_names
    )


class SelectedModelName(BaseModel):
    selected_model: str = Field(
        default_factory=get_selected_model_name
    )
