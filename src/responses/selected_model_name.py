from pydantic import BaseModel, Field

from src.summarizers.utils.model_selection import get_selected_model_name


class SelectedModelName(BaseModel):
    selected_model: str = Field(default_factory=get_selected_model_name)