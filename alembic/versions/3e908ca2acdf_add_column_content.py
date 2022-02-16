"""add column content

Revision ID: 3e908ca2acdf
Revises: c20c613e7548
Create Date: 2022-02-16 09:21:40.471095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e908ca2acdf'
down_revision = 'c20c613e7548'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass