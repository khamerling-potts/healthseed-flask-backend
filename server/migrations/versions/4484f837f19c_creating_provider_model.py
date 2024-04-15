"""creating provider model

Revision ID: 4484f837f19c
Revises: 71f6e13911a0
Create Date: 2024-04-15 12:28:50.466583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4484f837f19c'
down_revision = '71f6e13911a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('providers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_providers_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('providers')
    # ### end Alembic commands ###