"""adding notes to medications

Revision ID: fcff30ded890
Revises: 759c4c4a674f
Create Date: 2024-05-29 10:06:53.715861

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fcff30ded890'
down_revision = '759c4c4a674f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notes', sa.String(), nullable=True))

    with op.batch_alter_table('providers', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('routines', schema=None) as batch_op:
        batch_op.alter_column('times',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routines', schema=None) as batch_op:
        batch_op.alter_column('times',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)

    with op.batch_alter_table('providers', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('medications', schema=None) as batch_op:
        batch_op.drop_column('notes')

    # ### end Alembic commands ###