"""added credit period

Revision ID: 6714ff012763
Revises: 186591bff096
Create Date: 2025-06-19 14:13:07.689798

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6714ff012763"
down_revision: Union[str, Sequence[str], None] = "186591bff096"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "credits", sa.Column("cred_period", sa.Integer, server_default=sa.text("86400"))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("credits", "cred_period")
