"""renaming amount to dose

Revision ID: c61e18d625b1
Revises: f86b7a39c889
Create Date: 2024-04-22 15:02:23.980824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61e18d625b1'
down_revision = 'f86b7a39c889'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instructions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dose', sa.String(), nullable=False))
        batch_op.drop_column('amount')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instructions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('dose')

    # ### end Alembic commands ###
