from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"

    url: Mapped[str] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    content: Mapped[str]
    cluster_n: Mapped[int | None]

    summary = relationship(
        "Summary",
        back_populates="news",
        cascade="all, delete-orphan"
    )


class Summary(Base):
    __tablename__ = "summary"

    news_url: Mapped[str] = mapped_column(
        ForeignKey("news.url", ondelete="CASCADE", onupdate='CASCADE'),
        primary_key=True
    )
    content: Mapped[str]
    positive_rates: Mapped[int] = mapped_column(default=0)
    negative_rates: Mapped[int] = mapped_column(default=0)

    news = relationship(
        "News",
        back_populates="summary",
        single_parent=True
    )