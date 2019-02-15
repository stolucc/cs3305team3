"""empty message

Revision ID: dd2ab985218f
Revises: d3135a170b48
Create Date: 2019-02-14 18:44:23.688414

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dd2ab985218f'
down_revision = 'd3135a170b48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('researcher', sa.Column('ORCID', sa.Integer(), nullable=True))
    op.add_column('researcher', sa.Column('email', sa.String(length=80), nullable=True))
    op.add_column('researcher', sa.Column('f_name', sa.String(length=64), nullable=True))
    op.add_column('researcher', sa.Column('job_title', sa.String(length=4), nullable=True))
    op.add_column('researcher', sa.Column('l_name', sa.String(length=64), nullable=True))
    op.drop_constraint('user_profile_ibfk_1', 'user_profile', type_='foreignkey')
    op.drop_column('user_profile', 'login_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('login_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('user_profile_ibfk_1', 'user_profile', 'researcher', ['login_id'], ['researcher_id'])
    op.drop_column('researcher', 'l_name')
    op.drop_column('researcher', 'job_title')
    op.drop_column('researcher', 'f_name')
    op.drop_column('researcher', 'email')
    op.drop_column('researcher', 'ORCID')
    # ### end Alembic commands ###