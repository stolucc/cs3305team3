"""empty message

Revision ID: 5297021ac20d
Revises: 1b6248d5bf9d
Create Date: 2019-02-26 20:53:44.460685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5297021ac20d'
down_revision = '1b6248d5bf9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('call_for_proposals', sa.Column('call_for_proposal_title', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('call_for_proposals', 'call_for_proposal_title')
    # ### end Alembic commands ###
