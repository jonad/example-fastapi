"""Add foreign keys to post table

Revision ID: a1f3e9037b8b
Revises: 5219c72f6813
Create Date: 2025-07-01 17:42:39.962720

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1f3e9037b8b"
down_revision: Union[str, Sequence[str], None] = "5219c72f6813"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        "fk_posts_owner_id_users_id",
        "posts",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_posts_owner_id_users_id", "posts", type_="foreignkey")
    op.drop_column("posts", "owner_id")
    pass
