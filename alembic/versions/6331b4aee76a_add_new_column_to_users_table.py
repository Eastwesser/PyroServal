"""Add new column to users table

Revision ID: 6331b4aee76a
Revises: 5299436c57d9
Create Date: 2024-06-12 22:37:18.689965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6331b4aee76a'
down_revision: Union[str, None] = '5299436c57d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
