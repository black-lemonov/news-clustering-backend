from datetime import datetime

from pydantic import BaseModel


class SummaryScheme(BaseModel):
    title: str
    summary: str
    created_at: datetime
    cluster_n: int
    
    
class Pagination(BaseModel):
    page: int
    size: int
    total: int
    

class SummarySchemeWithPagination(BaseModel):
    data: list[SummaryScheme]
    pagination: Pagination
    
    
class SourceScheme(BaseModel):
    url: str
    title: str


class SummaryWithSourcesScheme(SummaryScheme):
    news: list[SourceScheme]

    