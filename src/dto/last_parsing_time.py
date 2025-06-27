from pydantic import BaseModel, Field

from src.services.bg_service import load_last_parsing_time_from_config


class LastParsingTime(BaseModel):
    last_parsing_time: str = Field(default_factory=lambda: load_last_parsing_time_from_config())