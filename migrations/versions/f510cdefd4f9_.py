"""empty message

Revision ID: f510cdefd4f9
Revises: f9b9a34a9b46
Create Date: 2019-03-11 14:21:10.673043

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f510cdefd4f9'
down_revision = 'f9b9a34a9b46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('call_for_proposals', 'duration_of_award',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=70),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'eligibility_criteria',
               existing_type=mysql.VARCHAR(length=60),
               type_=sa.String(length=70),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'reporting_guidelines',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=50),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'target_audience',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=80),
               existing_nullable=True)
    op.alter_column('grant_application', 'approved',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('grant_application', 'reviewer_approved',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('proposals_accepted', 'began',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('proposals_accepted', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('publications', 'in_press',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('publications', 'published',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('research_centre_admin', 'online',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('researcher_education', 'field_of_study',
               existing_type=mysql.VARCHAR(length=35),
               type_=sa.String(length=60),
               existing_nullable=True)
    op.alter_column('researcher_education', 'institution',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=60),
               existing_nullable=True)
    op.alter_column('researcher_education', 'location',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=60),
               existing_nullable=True)
    op.alter_column('researcher_profile', 'job_title',
               existing_type=mysql.VARCHAR(length=4),
               type_=sa.String(length=40),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('researcher_profile', 'job_title',
               existing_type=sa.String(length=40),
               type_=mysql.VARCHAR(length=4),
               existing_nullable=True)
    op.alter_column('researcher_education', 'location',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=45),
               existing_nullable=True)
    op.alter_column('researcher_education', 'institution',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=True)
    op.alter_column('researcher_education', 'field_of_study',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=35),
               existing_nullable=True)
    op.alter_column('research_centre_admin', 'online',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('publications', 'published',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('publications', 'in_press',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('proposals_accepted', 'confirmed',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('proposals_accepted', 'began',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('grant_application', 'reviewer_approved',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('grant_application', 'approved',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'target_audience',
               existing_type=sa.String(length=80),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'reporting_guidelines',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'eligibility_criteria',
               existing_type=sa.String(length=70),
               type_=mysql.VARCHAR(length=60),
               existing_nullable=True)
    op.alter_column('call_for_proposals', 'duration_of_award',
               existing_type=sa.String(length=70),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=True)
    # ### end Alembic commands ###