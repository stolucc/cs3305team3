"""empty message

Revision ID: 5b1f45458078
Revises: 6afc68d533a6
Create Date: 2019-03-04 01:09:45.486297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b1f45458078'
down_revision = '6afc68d533a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employment_db', sa.Column('users', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'employment_db', 'users', ['users'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employment_db', type_='foreignkey')
    op.drop_column('employment_db', 'users')
    # ### end Alembic commands ###
