from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models.base import Base


class Cluster(Base):
    __tablename__ = "cluster"

    n: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    news = relationship(
        "News",
        back_populates='cluster'
    )