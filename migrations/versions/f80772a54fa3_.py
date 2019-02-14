"""empty message

Revision ID: f80772a54fa3
Revises: f0c21e9210fe
Create Date: 2019-02-13 17:37:35.999057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f80772a54fa3'
down_revision = 'f0c21e9210fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('online', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'online')
    # ### end Alembic commands ###
