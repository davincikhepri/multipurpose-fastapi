"""add content column to posts table

Revision ID: 2c109f118f27
Revises: ef323db885fb
Create Date: 2024-11-05 11:47:15.672868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c109f118f27'
down_revision: Union[str, None] = 'ef323db885fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
