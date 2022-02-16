"""add all column to post table

Revision ID: 953fa8f83327
Revises: d6e099d26991
Create Date: 2022-02-16 09:33:28.578695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953fa8f83327'
down_revision = 'd6e099d26991'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
