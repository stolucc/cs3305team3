"""empty message

Revision ID: 6afc68d533a6
Revises: e29f955b6c89
Create Date: 2019-03-04 01:07:51.602763

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6afc68d533a6'
down_revision = 'e29f955b6c89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team_members', sa.Column('grant_reference', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'team_members', 'submitted_applications', ['grant_reference'], ['grant_application_id'])
    op.drop_column('team_members', 'grant_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team_members', sa.Column('grant_number', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'team_members', type_='foreignkey')
    op.drop_column('team_members', 'grant_reference')
    # ### end Alembic commands ###