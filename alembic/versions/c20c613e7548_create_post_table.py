"""create post table

Revision ID: c20c613e7548
Revises: 
Create Date: 2022-02-16 09:20:30.955821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c20c613e7548'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer,primary_key=True, nullable=False ), sa.Column('title', sa.String(), nullable = False))
    pass

def downgrade():
    op.drop_table('posts')
    pass