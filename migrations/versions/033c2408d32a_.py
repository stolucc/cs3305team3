"""empty message

Revision ID: 033c2408d32a
Revises: 49d6a69e7532
Create Date: 2019-02-15 12:28:50.714225

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '033c2408d32a'
down_revision = '49d6a69e7532'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('research_centre_profile')
    op.add_column('researcher', sa.Column('ORCID', sa.Integer(), nullable=True))
    op.add_column('researcher', sa.Column('email', sa.String(length=80), nullable=True))
    op.add_column('researcher', sa.Column('f_name', sa.String(length=64), nullable=True))
    op.add_column('researcher', sa.Column('job_title', sa.String(length=4), nullable=True))
    op.add_column('researcher', sa.Column('l_name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('researcher', 'l_name')
    op.drop_column('researcher', 'job_title')
    op.drop_column('researcher', 'f_name')
    op.drop_column('researcher', 'email')
    op.drop_column('researcher', 'ORCID')
    op.create_table('research_centre_profile',
    sa.Column('research_centre', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('research_centre_profile_ID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('online', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###