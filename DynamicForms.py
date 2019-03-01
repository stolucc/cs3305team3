from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, StringField, HiddenField, PasswordField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo
class GrantGeneralInfoForm(FlaskForm):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    proposal_title = StringField('Proposal Title', [validators.Length(min=1, max=300)], render_kw={"readonly": True})
    award_duration = StringField('Award Duration', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Researcher, Research Body, University"})
    national_research_priority = StringField('National Research Priority', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Proven track record with funding"})
    sfi_legal_remit_justification = StringField('SFI Legal Justification', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Duration in months"})
    ethical_issues = StringField('Ethical Issues', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Monthly/Annual Reports"})
    applicants_country = StringField('Applicants Country', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

class GrantScientificAbstractForm(FlaskForm):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    scientific_abstract = StringField('Scientific Abstract', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

class GrantLayAbstractForm(FlaskForm):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    lay_abstract = StringField('Lay Abstract', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

