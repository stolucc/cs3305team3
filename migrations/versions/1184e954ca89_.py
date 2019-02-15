"""empty message

Revision ID: 1184e954ca89
Revises: 033c2408d32a
Create Date: 2019-02-15 12:35:26.682811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1184e954ca89'
down_revision = '033c2408d32a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user__profile2',
    sa.Column('user_id2', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('online', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('user_id2')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user__profile2')
    # ### end Alembic commands ###