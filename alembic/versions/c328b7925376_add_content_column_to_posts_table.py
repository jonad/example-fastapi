"""add content column to posts table

Revision ID: c328b7925376
Revises: d44072f05b70
Create Date: 2025-07-01 17:29:45.832396

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c328b7925376"
down_revision: Union[str, Sequence[str], None] = "d44072f05b70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False, server_default=""),
    )
    op.alter_column(
        "posts", "content", server_default=None
    )  # Remove default value after adding column
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
