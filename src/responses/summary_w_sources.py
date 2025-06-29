from src.dto.source import Source
from src.dto.summary import SummaryDTO


class SummaryWithSources(SummaryDTO):
    news: list[Source]

    @classmethod
    def from_summary_w_list(cls, summary: SummaryDTO, sources: list[Source]):
        return cls(
            title=summary.title,
            content=summary.content,
            created_at=summary.created_at,
            cluster_n=summary.cluster_n,
            news=sources
        )
