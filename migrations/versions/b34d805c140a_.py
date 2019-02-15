"""empty message

Revision ID: b34d805c140a
Revises: ffb9f9eb2f0c
Create Date: 2019-02-15 16:33:46.881277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b34d805c140a'
down_revision = 'ffb9f9eb2f0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviewer', sa.Column('loginID', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reviewer', 'login_account', ['loginID'], ['login_account_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reviewer', type_='foreignkey')
    op.drop_column('reviewer', 'loginID')
    # ### end Alembic commands ###
