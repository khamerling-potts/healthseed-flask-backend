"""changing routine time to times array

Revision ID: 1307ee4624e9
Revises: cb3d77703c4a
Create Date: 2024-04-29 11:03:55.639561

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1307ee4624e9'
down_revision = 'cb3d77703c4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routines', schema=None) as batch_op:
        batch_op.add_column(sa.Column('times', postgresql.ARRAY(sa.String()), nullable=True))
        batch_op.drop_column('time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routines', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('times')

    # ### end Alembic commands ###