"""add content column to post table

Revision ID: 896ece4596dd
Revises: da453f38a600
Create Date: 2024-03-04 02:36:44.210964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '896ece4596dd'
down_revision: Union[str, None] = 'da453f38a600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
