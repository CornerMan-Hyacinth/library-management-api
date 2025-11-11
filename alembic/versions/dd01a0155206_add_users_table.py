"""add users table

Revision ID: dd01a0155206
Revises: 6230e3844af9
Create Date: 2025-11-10 08:27:35.249175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd01a0155206'
down_revision: Union[str, Sequence[str], None] = '6230e3844af9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
