"""empty message

Revision ID: 9e6de2612822
Revises: 8347147023a3
Create Date: 2019-02-16 02:16:12.048560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e6de2612822'
down_revision = '8347147023a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('call_for_proposals', sa.Column('deadline', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('call_for_proposals', 'deadline')
    # ### end Alembic commands ###