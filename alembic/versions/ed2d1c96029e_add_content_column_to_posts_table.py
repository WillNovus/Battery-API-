"""add content column to posts table

Revision ID: ed2d1c96029e
Revises: d2f59805b47a
Create Date: 2022-11-23 23:35:12.693796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed2d1c96029e'
down_revision = 'd2f59805b47a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('Content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'Content')
    pass