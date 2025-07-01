import math

from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    page: int = Field(default=1, ge=1, description="Номер страницы")
    size: int = Field(default=5, ge=0, description="Кол-во элементов на странице")


class PaginationResponse(PaginationRequest):
    total: int = Field(
        default_factory=lambda data: (
            math.ceil(data["total_count"] / data["size"]) if data["size"] > 0 else 0
        )
    )
