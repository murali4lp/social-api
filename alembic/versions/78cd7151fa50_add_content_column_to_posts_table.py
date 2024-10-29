"""add content column to posts table

Revision ID: 78cd7151fa50
Revises: 35155cd6b727
Create Date: 2024-10-30 02:59:16.449205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78cd7151fa50'
down_revision: Union[str, None] = '35155cd6b727'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
