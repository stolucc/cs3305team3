"""empty message

Revision ID: 66eb78fa61a0
Revises: 1ffb6ceffcb8
Create Date: 2019-02-15 23:48:26.494307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66eb78fa61a0'
down_revision = '1ffb6ceffcb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('awards_db',
    sa.Column('awards_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('awarding_body', sa.String(length=21), nullable=True),
    sa.Column('awarding_details', sa.String(length=100), nullable=True),
    sa.Column('member_name', sa.String(length=21), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('research_Profile', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['research_Profile'], ['researcher_profile.researcher_id'], ),
    sa.PrimaryKeyConstraint('awards_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('awards_db')
    # ### end Alembic commands ###
