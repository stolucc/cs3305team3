"""empty message

Revision ID: e15582747147
Revises: a0cfe53e4762
Create Date: 2019-02-13 18:06:48.038571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e15582747147'
down_revision = 'a0cfe53e4762'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviewer',
    sa.Column('sfi_admin_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('sfi_admin_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviewer')
    # ### end Alembic commands ###