from wtforms import Form, IntegerField, StringField, PasswordField, BooleanField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo

class ResetPasswordRequestForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=45)])

class ResetPasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class DeletionForm(Form):
    user_id = IntegerField('User ID', [validators.NumberRange(min=0, max=999)])

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=45)])
    user_type = SelectField(u'User Type', choices=[
        ('sfiAdmin', 'SFI Admin'),
        ('researcher', 'Researcher'),
        ('researchCentre', 'Research Centre'),
        ('reviewer', 'Reviewer'),
        ('institution', 'Institution')])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class AddProposalForm(Form):
    text_of_call = StringField('Text of Call', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Text of call"})
    target_audience = StringField('Target Audience', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Researcher, Research Body, University"})
    eligibility_criteria = StringField('Eligibility Criteria', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Proven track record with funding"})
    duration_of_award = StringField('Duration of Award', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Duration in months"})
    reporting_guidelines = StringField('Reporting Guidelines', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Monthly/Annual Reports"})
    start_date = StringField('Start Date', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    deadline = StringField('Deadline', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

class ProfileForm(Form):
    #Education
    orcid = StringField('ORCID', [validators.Length(min=19, max=19)])
    degree = StringField('Degree', [validators.Length(min=4, max=30)])
    field_of_study = StringField('Field of Study', [validators.Length(min=4, max=30)])
    institution = StringField('Institution', [validators.Length(min=2, max=30)])
    location = StringField('Location', [validators.Length(min=2, max=30)])
    year_of_degree_award = StringField('Year Degree Awarded', [validators.Length(min=2, max=30)])
    #Employment
    employment_faculty = StringField('Place of Employment', [validators.Length(min=1, max=30)])
    location = StringField('Location', [validators.Length(min=1, max=30)])
    years_of_employment = StringField('Years of Employment', [validators.Length(min=1, max=30)])

class GeneralForm(Form):
    fName = StringField('Firstname', [validators.Length(min=4, max=30)])
    lName = StringField('Lastname', [validators.Length(min=4, max=30)])
    jobTitle = StringField('Job Title', [validators.Length(min=2, max=30)])
    prefix = StringField('Prefix', [validators.Length(min=2, max=30)])
    suffix = StringField('Suffix', [validators.Length(min=2, max=30)])
    phone = StringField('Phone', [validators.Length(min=2, max=30)])
    phoneExtension = StringField('Phone Extension', [validators.Length(min=2, max=30)])
    email = StringField('Email', [validators.Length(min=2, max=30)])
    orcid= StringField('ORCID', [validators.Length(min=19, max=19)])

class EducationForm(Form):
    degree = StringField('Degree', [validators.Length(min=4, max=30)])
    field_of_study = StringField('Field of Study', [validators.Length(min=4, max=30)])
    institution = StringField('Institution', [validators.Length(min=2, max=30)])
    location = StringField('Location', [validators.Length(min=2, max=30)])
    year_degree_awarded = StringField('Year Degree Awarded', [validators.Length(min=2, max=30)])