"""empty message

Revision ID: df2d099c60f6
Revises: 94e78eeb1a17
Create Date: 2019-03-06 14:28:47.921504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df2d099c60f6'
down_revision = '94e78eeb1a17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('engagements', sa.Column('users', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'engagements', 'users', ['users'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'engagements', type_='foreignkey')
    op.drop_column('engagements', 'users')
    # ### end Alembic commands ###