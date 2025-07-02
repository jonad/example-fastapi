"""Add lasts few columns to posts table

Revision ID: 9701ab6dd674
Revises: a1f3e9037b8b
Create Date: 2025-07-01 17:46:06.752310

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9701ab6dd674"
down_revision: Union[str, Sequence[str], None] = "a1f3e9037b8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.add_column(
        "posts",
        sa.Column(
            "published", sa.Boolean(), server_default=sa.sql.expression.true(), nullable=False
        ),
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
