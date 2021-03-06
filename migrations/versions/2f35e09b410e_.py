"""empty message

Revision ID: 2f35e09b410e
Revises: d8fbb6ec0214
Create Date: 2019-03-06 15:33:17.507437

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2f35e09b410e'
down_revision = 'd8fbb6ec0214'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professional_societies',
    sa.Column('research_profile_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('membership_type', sa.String(length=64), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('research_Profile', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['research_Profile'], ['researcher_profile.researcher_id'], ),
    sa.PrimaryKeyConstraint('research_profile_id')
    )
    op.drop_table('professional_socities')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professional_socities',
    sa.Column('research_profile_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('start_date', mysql.DATETIME(), nullable=True),
    sa.Column('end_date', mysql.DATETIME(), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('membership_type', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('research_Profile', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['research_Profile'], ['researcher_profile.researcher_id'], name='professional_socities_ibfk_1'),
    sa.PrimaryKeyConstraint('research_profile_id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('professional_societies')
    # ### end Alembic commands ###
