from pydantic import BaseModel

from src.dto.summary import SummaryDTO
from src.responses.pagination import Pagination


class SummariesListWithPagination(BaseModel):
    summaries: list[SummaryDTO]
    pagination: Pagination

    @classmethod
    def from_summaries(cls, summaries: list[SummaryDTO], page: int, size: int):
        return cls(
            summaries=summaries,
            pagination=Pagination(page=page, size=size, total=len(summaries))
        )
