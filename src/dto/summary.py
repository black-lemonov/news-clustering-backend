from datetime import datetime

from pydantic import BaseModel


class SummaryDTO(BaseModel):
    title: str
    content: str
    created_at: datetime
    cluster_n: int