"""empty message

Revision ID: d3135a170b48
Revises: cf437813bd4a
Create Date: 2019-02-13 18:45:21.190541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3135a170b48'
down_revision = 'cf437813bd4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profile',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('online', sa.BOOLEAN(), nullable=True),
    sa.Column('login_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['login_id'], ['researcher.researcher_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.add_column('research_centre', sa.Column('user_profile_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'research_centre', 'user_profile', ['user_profile_id'], ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'research_centre', type_='foreignkey')
    op.drop_column('research_centre', 'user_profile_id')
    op.drop_table('user_profile')
    # ### end Alembic commands ###