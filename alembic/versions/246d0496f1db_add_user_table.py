"""add  user table

Revision ID: 246d0496f1db
Revises: 3e908ca2acdf
Create Date: 2022-02-16 09:25:58.047306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '246d0496f1db'
down_revision = '3e908ca2acdf'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass