from datetime import datetime

from pydantic import BaseModel


class NewsDTO(BaseModel):
    url: str
    title: str
    content: str
    date: datetime
