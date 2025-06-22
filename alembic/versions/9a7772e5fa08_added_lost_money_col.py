"""added lost_money col

Revision ID: 9a7772e5fa08
Revises: 6714ff012763
Create Date: 2025-06-22 11:24:09.367541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a7772e5fa08'
down_revision: Union[str, Sequence[str], None] = '6714ff012763'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("lost_money", sa.Integer, server_default="0"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "lost_money")
