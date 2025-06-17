"""added prefix

Revision ID: 90d379ae6851
Revises: 
Create Date: 2025-06-17 15:49:50.488445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90d379ae6851'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',
                 sa.Column('prefix', sa.String, nullable=False, server_default='')
                 )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'prefix')
