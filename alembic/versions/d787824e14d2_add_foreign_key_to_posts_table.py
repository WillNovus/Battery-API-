"""add foreign-key to posts table

Revision ID: d787824e14d2
Revises: c04e328109f3
Create Date: 2022-11-27 15:58:06.306521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd787824e14d2'
down_revision = 'c04e328109f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table ='posts', referent_table='users', local_cols = ['owner_id'],
                            remote_cols= ['id'], ondelete = "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name ="posts")
    op.drop_column('posts', 'owner_id')
    pass
