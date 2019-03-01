"""empty message

Revision ID: fe8a1ee2d17a
Revises: 201a0e76c25a
Create Date: 2019-02-24 15:51:16.612758

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fe8a1ee2d17a'
down_revision = '201a0e76c25a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grant_application', sa.Column('applicants_country', sa.String(length=40), nullable=True))
    op.add_column('grant_application', sa.Column('award_duration', sa.String(length=30), nullable=True))
    op.add_column('grant_application', sa.Column('ethical_issues', sa.String(length=200), nullable=True))
    op.add_column('grant_application', sa.Column('lay_abstract', sa.String(length=1000), nullable=True))
    op.add_column('grant_application', sa.Column('national_research_priority', sa.String(length=60), nullable=True))
    op.add_column('grant_application', sa.Column('programme_documents', sa.String(length=1000), nullable=True))
    op.add_column('grant_application', sa.Column('proposal_title', sa.String(length=30), nullable=True))
    op.add_column('grant_application', sa.Column('scientific_abstract', sa.String(length=2000), nullable=True))
    op.add_column('grant_application', sa.Column('sfi_legal_remit_justification', sa.String(length=2000), nullable=True))
    op.drop_column('grant_application', 'scientificAbstract')
    op.drop_column('grant_application', 'layAbstract')
    op.drop_column('grant_application', 'nationalResearchPriority')
    op.drop_column('grant_application', 'applicantsCountry')
    op.drop_column('grant_application', 'proposalTitle')
    op.drop_column('grant_application', 'awardDuration')
    op.drop_column('grant_application', 'ethicalIssues')
    op.drop_column('grant_application', 'sfiLegalRemitJustification')
    op.drop_column('grant_application', 'programmeDocuments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grant_application', sa.Column('programmeDocuments', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('grant_application', sa.Column('sfiLegalRemitJustification', mysql.VARCHAR(length=2000), nullable=True))
    op.add_column('grant_application', sa.Column('ethicalIssues', mysql.VARCHAR(length=200), nullable=True))
    op.add_column('grant_application', sa.Column('awardDuration', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('grant_application', sa.Column('proposalTitle', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('grant_application', sa.Column('applicantsCountry', mysql.VARCHAR(length=40), nullable=True))
    op.add_column('grant_application', sa.Column('nationalResearchPriority', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('grant_application', sa.Column('layAbstract', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('grant_application', sa.Column('scientificAbstract', mysql.VARCHAR(length=2000), nullable=True))
    op.drop_column('grant_application', 'sfi_legal_remit_justification')
    op.drop_column('grant_application', 'scientific_abstract')
    op.drop_column('grant_application', 'proposal_title')
    op.drop_column('grant_application', 'programme_documents')
    op.drop_column('grant_application', 'national_research_priority')
    op.drop_column('grant_application', 'lay_abstract')
    op.drop_column('grant_application', 'ethical_issues')
    op.drop_column('grant_application', 'award_duration')
    op.drop_column('grant_application', 'applicants_country')
    # ### end Alembic commands ###