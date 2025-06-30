from datetime import datetime

from fastapi.responses import Response
from pydantic import BaseModel

from src.pagination import PaginationResponse


class Summary(BaseModel):
    title: str
    content: str
    created_at: datetime
    cluster_n: int


class SummariesListWithPagination(BaseModel):
    summaries: list[Summary]
    pagination: PaginationResponse

    @classmethod
    def from_summaries(cls, summaries: list[Summary], page: int, size: int):
        return cls(
            summaries=summaries,
            pagination=PaginationResponse(page=page, size=size, total=len(summaries))
        )


class Source(BaseModel):
    url: str
    title: str


class SummaryWithSources(Summary):
    news: list[Source]

    @classmethod
    def from_summary_w_list(cls, summary: Summary, sources: list[Source]):
        return cls(
            title=summary.title,
            content=summary.content,
            created_at=summary.created_at,
            cluster_n=summary.cluster_n,
            news=sources
        )


class NewsCSVTable(Response):
    table_filename = "news_with_summaries.csv"
    media_type = "text/csv",
    headers = {
        "Content-Disposition": f"attachment; filename={table_filename}",
        "Content-Type": "text/csv; charset=utf-8"
    }
