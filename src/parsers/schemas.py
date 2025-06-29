from datetime import datetime

from pydantic import BaseModel, Field

from src.parsers.utils import get_parsers_sites_urls, load_last_parsing_time_from_config


class ParsersSitesUrls(BaseModel):
    sites_urls: list[str] = Field(
        default_factory=get_parsers_sites_urls
    )
    

class LastParsingTime(BaseModel):
    last_parsing_time: str = Field(
        default_factory=load_last_parsing_time_from_config
    )


class News(BaseModel):
    url: str
    title: str
    content: str
    date: datetime