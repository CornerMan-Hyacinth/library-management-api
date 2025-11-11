"""add users table

Revision ID: 6230e3844af9
Revises: cbe2a193ab6b
Create Date: 2025-11-10 08:27:23.548372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6230e3844af9'
down_revision: Union[str, Sequence[str], None] = 'cbe2a193ab6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
