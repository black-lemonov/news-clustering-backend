from datetime import datetime
from dataclasses import dataclass

@dataclass
class News:
    url: str
    title: str
    content: str
    date: datetime