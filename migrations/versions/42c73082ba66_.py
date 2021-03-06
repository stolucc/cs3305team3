"""empty message

Revision ID: 42c73082ba66
Revises: 5b1f45458078
Create Date: 2019-03-04 01:13:13.412226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42c73082ba66'
down_revision = '5b1f45458078'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('academic_collaborations', sa.Column('users', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'academic_collaborations', 'users', ['users'], ['id'])
    op.add_column('publications', sa.Column('users', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'publications', 'users', ['users'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'publications', type_='foreignkey')
    op.drop_column('publications', 'users')
    op.drop_constraint(None, 'academic_collaborations', type_='foreignkey')
    op.drop_column('academic_collaborations', 'users')
    # ### end Alembic commands ###
