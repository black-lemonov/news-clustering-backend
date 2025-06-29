from pydantic import BaseModel, Field

from src.services.parsers_service import get_parsers_sites_urls


class ParsersSitesUrls(BaseModel):
    sites_urls: list[str] = Field(default_factory=get_parsers_sites_urls)