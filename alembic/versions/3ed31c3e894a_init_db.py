"""init_db

Revision ID: 3ed31c3e894a
Revises:
Create Date: 2025-07-05 21:01:29.508861

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ed31c3e894a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "news",
        sa.Column("url", sa.String, primary_key=True, index=True),
        sa.Column("title", sa.String),
        sa.Column("published_at", sa.DateTime(timezone=True), index=True),
        sa.Column("content", sa.String),
        sa.Column("cluster_n", sa.Integer, nullable=True),
    )

    op.create_table(
        "summary",
        sa.Column(
            "news_url",
            sa.String,
            sa.ForeignKey("news.url", ondelete="CASCADE", onupdate="CASCADE"),
            primary_key=True,
        ),
        sa.Column("content", sa.String),
        sa.Column("positive_rates", sa.Integer, default=0),
        sa.Column("negative_rates", sa.Integer, default=0),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("summary")
    op.drop_table("news")
