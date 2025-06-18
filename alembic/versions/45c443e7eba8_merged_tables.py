"""merged tables

Revision ID: 45c443e7eba8
Revises: 90d379ae6851
Create Date: 2025-06-18 18:43:33.539102

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45c443e7eba8"
down_revision: Union[str, Sequence[str], None] = "90d379ae6851"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("dodep_date", sa.Integer, default=0))
    op.add_column("users", sa.Column("visit_date", sa.Integer, default=0))

    op.execute(
        """
        UPDATE users 
        SET dodep_date = (SELECT date FROM dates WHERE dates.id = users.id)
    """
    )
    op.execute(
        """
        UPDATE users 
        SET visit_date = (SELECT date FROM visitors WHERE visitors.id = users.id)
    """
    )

    op.drop_table("dates")
    op.drop_table("visitors")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "dates",
        sa.Column("id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("date", sa.Integer, default=0),
    )
    op.create_table(
        "visitors",
        sa.Column("id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("date", sa.Integer, default=0),
    )

    op.execute(
        """
        INSERT INTO dates (id, date)
        SELECT id, dodep_date FROM users
    """
    )
    op.execute(
        """
        INSERT INTO visitors (id, date)
        SELECT id, visit_date FROM users
    """
    )

    op.drop_column("users", "dodep_date")
    op.drop_column("users", "visit_date")
