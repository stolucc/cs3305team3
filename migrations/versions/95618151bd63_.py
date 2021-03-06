"""empty message

Revision ID: 95618151bd63
Revises: d0f15ee01d1a
Create Date: 2019-02-28 18:47:57.442494

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '95618151bd63'
down_revision = 'd0f15ee01d1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coapplicants_db',
    sa.Column('coapplicant_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('organization', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('grant_application', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grant_application'], ['grant_application.grant_application_id'], ),
    sa.PrimaryKeyConstraint('coapplicant_id')
    )
    op.create_table('collaborators_db',
    sa.Column('collaborator_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('organization', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('grant_application', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grant_application'], ['grant_application.grant_application_id'], ),
    sa.PrimaryKeyConstraint('collaborator_id')
    )
    op.drop_table('co__applicants')
    op.drop_table('collaborators')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collaborators',
    sa.Column('name', mysql.VARCHAR(length=60), nullable=True),
    sa.Column('organization', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('grant_application', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('collaborator_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['grant_application'], ['grant_application.grant_application_id'], name='collaborators_ibfk_1'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('co__applicants',
    sa.Column('coapplicant_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=60), nullable=True),
    sa.Column('organization', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('grant_application', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['grant_application'], ['grant_application.grant_application_id'], name='co__applicants_ibfk_1'),
    sa.PrimaryKeyConstraint('coapplicant_id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('collaborators_db')
    op.drop_table('coapplicants_db')
    # ### end Alembic commands ###
