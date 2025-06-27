import math

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int
    size: int
    total: int = Field(
        default_factory=lambda data: (
            math.ceil(data["total_count"] / data["size"])
            if data["size"] > 0 else 0
        )
    )