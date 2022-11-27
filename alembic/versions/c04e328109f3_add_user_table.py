"""add user table

Revision ID: c04e328109f3
Revises: ed2d1c96029e
Create Date: 2022-11-27 14:44:01.420869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04e328109f3'
down_revision = 'ed2d1c96029e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('passsword', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                server_default= sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
