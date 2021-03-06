"""empty message

Revision ID: ac5647e3093a
Revises: df2d099c60f6
Create Date: 2019-03-06 14:44:51.118738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac5647e3093a'
down_revision = 'df2d099c60f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conferences', sa.Column('users', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'conferences', 'users', ['users'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'conferences', type_='foreignkey')
    op.drop_column('conferences', 'users')
    # ### end Alembic commands ###
