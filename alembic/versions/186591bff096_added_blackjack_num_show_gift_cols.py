"""added blackjack_num&show_gift cols

Revision ID: 186591bff096
Revises: 45c443e7eba8
Create Date: 2025-06-19 00:45:51.740012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '186591bff096'
down_revision: Union[str, Sequence[str], None] = '45c443e7eba8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("blackjack_num", sa.Integer, default=0))
    op.add_column("gifts", sa.Column("show_gift", sa.Boolean, nullable=False, server_default=sa.text("true")))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "blackjack_num")
    op.drop_column("gifts", "show_gift")
