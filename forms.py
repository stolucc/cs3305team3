from wtforms import Form, IntegerField, StringField, DateField, PasswordField, BooleanField, RadioField, SelectField, SubmitField, HiddenField, validators
from wtforms.validators import DataRequired, Email, EqualTo

class ResetPasswordRequestForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=45), validators.Email()], render_kw={"placeholder": "Please enter your email to reset your password"})

class ResetPasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "New password"})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-enter new password"})
    submit = SubmitField('Request Password Reset')

class DeletionForm(Form):
    user_id = IntegerField('User ID', [validators.NumberRange(min=0, max=999)], render_kw={"placeholder": "Enter the user ID to remove"})

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=25)], render_kw={"placeholder": "Please enter a username"})
    email = StringField('Email Address', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Please enter an email"})
    user_type = SelectField(u'User Type', choices=[
        ('sfiAdmin', 'SFI Admin'),
        ('researcher', 'Researcher'),
        ('researchCentre', 'Research Centre'),
        ('reviewer', 'Reviewer'),
        ('institution', 'Institution')])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Please enter a password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Please re-enter the password"})
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=25)], render_kw={"placeholder": "Please enter a username"})
    email = StringField('Email Address', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Please enter an email"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Please enter a password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Please re-enter the password"})
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class AddProposalForm(Form):
    text_of_call = StringField('Text of Call', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Text of call"})
    call_for_proposal_title = StringField('Title of call for proposal', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Title of call for proposal"})
    target_audience = StringField('Target Audience', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Target Audience, e.g. Researcher, Research Body, University"})
    eligibility_criteria = StringField('Eligibility Criteria', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Proven track record with funding"})
    duration_of_award = StringField('Duration of Award', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Duration in months"})
    reporting_guidelines = StringField('Reporting Guidelines', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Monthly/Annual Reports"})
    start_date = StringField('Start Date', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    deadline = StringField('Deadline', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

class AddGrantApplicationForm(Form):
    proposal_title = StringField('Proposal Title', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Text of call"})
    award_duration = StringField('Award Duration', [validators.Length(min=6, max=450)], render_kw={"placeholder": "Researcher, Research Body, University"})
    national_research_priority = StringField('National Research Priority', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Proven track record with funding"})
    sfi_legal_remit_justification = StringField('SFI Legal Justification', [validators.Length(min=6, max=300)], render_kw={"placeholder": "Duration in months"})
    ethical_issues = StringField('Ethical Issues', [validators.Length(min=6, max=300)], render_kw={"placeholder": "Monthly/Annual Reports"})
    applicants_country = StringField('Applicants Country', [validators.Length(min=6, max=300)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    scientific_abstract = StringField('Scientific Abstract', [validators.Length(min=6, max=300)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    lay_abstract = StringField('Lay Abstract', [validators.Length(min=6, max=300)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    #programme_documents = StringField('', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    #Have to add forms for applicants and coapplicants
    #   Have to add URL for uploaded document

class GrantGeneralInfoForm(Form):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    proposal_title = StringField('Proposal Title', [validators.Length(min=1, max=300)], render_kw={"readonly": True})
    award_duration = StringField('Award Duration', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Researcher, Research Body, University"})
    national_research_priority = StringField('National Research Priority', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Proven track record with funding"})
    sfi_legal_remit_justification = StringField('SFI Legal Justification', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Duration in months"})
    ethical_issues = StringField('Ethical Issues', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Monthly/Annual Reports"})
    applicants_country = StringField('Applicants Country', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

class GrantScientificAbstractForm(Form):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    scientific_abstract = StringField('Scientific Abstract', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

class GrantLayAbstractForm(Form):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    lay_abstract = StringField('Lay Abstract', [validators.Length(min=6, max=30)], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

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

class AddOrcid(Form):
    orcid = StringField('ORCID', [validators.Length(min=19, max=19)], render_kw={"placeholder": "****-****-****-****"})

class GeneralForm(Form):
    f_name = StringField('Firstname', [validators.Length(min=2, max=30)], render_kw={"placeholder": "Please enter your firstname(s)"})
    l_name = StringField('Lastname', [validators.Length(min=2, max=30)], render_kw={"placeholder": "Please enter your lastname"})
    job_title = StringField('Job Title', [validators.Length(min=0, max=30)], render_kw={"placeholder": "Please enter your job title"})
    prefix = StringField('Prefix', [validators.Length(min=0, max=30)], render_kw={"placeholder": "Please enter your prefix"})
    suffix = StringField('Suffix', [validators.Length(min=0, max=30)], render_kw={"placeholder": "Please enter your suffix"})
    phone = StringField('Phone', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Please enter your contact number"})
    phone_extension = StringField('Phone Extension', [validators.Length(min=2, max=30)], render_kw={"placeholder": "Please enter the phone extension of your contact number"})

class GeneralUpdateForm(Form):
    fName = StringField('Firstname', [validators.Length(min=1, max=30)])
    lName = StringField('Lastname', [validators.Length(min=1, max=30)])
    jobTitle = StringField('Job Title', [validators.Length(min=2, max=30)])
    prefix = StringField('Prefix', [validators.Length(min=2, max=30)])
    suffix = StringField('Suffix', [validators.Length(min=0, max=30)])
    phone = StringField('Phone', [validators.Length(min=2, max=30)])
    phoneExtension = StringField('Phone Extension', [validators.Length(min=2, max=30)])

    submit=SubmitField('Edit')

class EducationForm(Form):
    degree = StringField('Degree Type (bsc/msc.. etc) :', [validators.Length(min=0, max=30)], render_kw={"placeholder": "e.g. PhD, MSc, BSc"})
    field_of_study = StringField('Field of Study:', [validators.Length(min=0, max=60)], render_kw={"placeholder": "e.g. Computer Science"})
    institution = StringField('Institution Name:', [validators.Length(min=2, max=60)], render_kw={"placeholder": "e.g. University College Cork"})
    location = StringField('Location : ', [validators.Length(min=2, max=60)], render_kw={"placeholder": "e.g. Cork, Ireland"})
    year_of_degree = StringField('Year Degree Awarded :', [validators.Length(min=4, max=4)], render_kw={"placeholder": "YYYY"})

class EducationFormAdd(Form):
    degree = StringField('Degree Type (bsc/msc.. etc) :', [validators.Length(min=2, max=30)])
    field_of_study = StringField('Field of Study:', [validators.Length(min=3, max=40)])
    institution = StringField('Institution Name:', [validators.Length(min=2, max=30)])
    location = StringField('Location : ', [validators.Length(min=2, max=30)])
    year_of_degree = StringField('Year Degree Awarded :', [validators.Length(min=2, max=30)])

class TeamMembersForm(Form):
    start_date = DateField('Start date :')
    departure_date = DateField('End date with member :')
    name = StringField('Name of Member :', [validators.Length(min=2, max=30)])
    position = StringField('Position of Member :', [validators.Length(min=3, max=30)])

class EmploymentForm(Form):
    institution = StringField('Name of institution :', [validators.Length(min=2, max=30)])
    location = StringField('Location of institution :', [validators.Length(min=2, max=30)], render_kw={"placeholder": "e.g. Cork, Ireland"})
    year = StringField('First Year at this institution :', [validators.Length(min=4, max=4)], render_kw={"placeholder": "YYYY"})

class ProfessionalSocietiesForm(Form):
    start_date = DateField('Start date at society :', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End date at society :', render_kw={"placeholder": "YYYY-MM-DD"})
    name = StringField('Name of society :', [validators.Length(min=2, max=30)], render_kw={"placeholder": "e.g. Engineers Ireland"})
    membership_type = StringField('Membership type :', [validators.Length(min=3, max=30)], render_kw={"placeholder": "e.g. Academic"})
    status = StringField('Status :', [validators.Length(min=3, max=30)], render_kw={"placeholder": "e.g. Present"})

class AwardsForm(Form):
    awarding_body = StringField('Awarding Body :', [validators.Length(min=2, max=30)])
    awarding_details = StringField('Details of the award :', [validators.Length(min=4, max=60)])
    year = StringField('Year awarded :', [validators.Length(min=4, max=4)], render_kw={"placeholder": "2017"})

class FundingDiversificationForm(Form):
    start_date = DateField('Start date :', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End date :', render_kw={"placeholder": "YYYY-MM-DD"})
    funding_amount = StringField('Funding Amount (€) :', [validators.Length(min=1, max=10)], render_kw={"placeholder": "e.g. 20000"})
    funding_body = StringField('Funding Body:', [validators.Length(min=2, max=30)], render_kw={"placeholder": "e.g. SFI"})
    funding_programme = StringField('Funding Programme :', [validators.Length(min=2, max=30)], render_kw={"placeholder": "e.g. ERC"})
    status = StringField('Funding Status :', [validators.Length(min=2, max=30)], render_kw={"placeholder": "e.g. Complete"})
    #primary_attribution = StringField('Primary attribution :', [validators.Length(min=2, max=30)])

class ImpactsForm(Form):
    impact_title = StringField('Title of Impact :', [validators.Length(min=4, max=20)])
    impact_category = StringField('Category of Impact :', [validators.Length(min=3, max=20)])
    primary_beneficiary = StringField('Primary Beneficiary :', [validators.Length(min=4, max=20)])
    #primary_attribution = StringField('Primary Attribution :', [validators.Length(min=4, max=20)])

class InnovationsForm(Form):
    year = IntegerField('Year :', render_kw={"placeholder": "YYYY"})
    type = StringField('Type :', [validators.Length(min=4, max=30)])
    title = StringField('Title :', [validators.Length(min=4, max=30)])


class PublicationsForm(Form):
    year = IntegerField('Publication Year :', render_kw={"placeholder": "YYYY"})
    title = StringField('Publication Title :', [validators.Length(min=4, max=40)])
    type = StringField('Publication Type :', [validators.Length(min=4, max=20)])
    journal_conference_name = StringField('Journal/Conference Name :', [validators.Length(min=4, max=30)])
    #published = RadioField('Published :Yes/No', choices=[(True, 'Yes'), (False, 'No')], default=False)
    #in_press = RadioField('In Press :Yes/No', choices=[(True, 'Yes'), (False, 'No')], default=False)
    published = SelectField(u'Published :', choices=[
        ('True', 'Yes'),
        ('False', 'No')])
    in_press = SelectField(u'In Press :', choices=[
        ('True', 'Yes'),
        ('False', 'No')])
    doi = StringField('DOI :')

class PresentationsForm(Form):
    year = IntegerField('Year :', render_kw={"placeholder": "YYYY"})
    type = StringField('Type :', [validators.Length(min=4, max=20)])
    title = StringField('Title of Presenatation :', [validators.Length(min=4, max=20)])
    organizing_body = StringField('Organizing body :', [validators.Length(min=4, max=20)])
    location = StringField('Location of presentation :', [validators.Length(min=4, max=20)])

class AcademicCollabForm(Form):
    start_date = DateField('Start date :', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End date :', render_kw={"placeholder": "YYYY-MM-DD"})
    department = StringField('Department :', [validators.Length(min=4, max=20)])
    institution_name = StringField('Institution name :', [validators.Length(min=4, max=20)])
    location = StringField('Location :', [validators.Length(min=4, max=20)])
    collaborator_name = StringField('Collaborator name :', [validators.Length(min=4, max=20)])
    collaborator_goal = StringField('Collaborator goal :', [validators.Length(min=4, max=20)])
    interaction_frequency = StringField(' Interaction frequency :', [validators.Length(min=4, max=20)])
    grant_num = IntegerField('Grant Number :', [validators.Length(min=0, max=20)])

class NonAcademicCollabForm(Form):
    start_date = DateField('Start date :', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End date :', render_kw={"placeholder": "YYYY-MM-DD"})
    department = StringField('Department :', [validators.Length(min=2, max=20)])
    location = StringField('Location :', [validators.Length(min=3, max=20)])
    collaborator_name = StringField('Collaborator name :', [validators.Length(min=2, max=20)])
    collaborator_goal = StringField('Collaborator goal :', [validators.Length(min=4, max=20)])
    interaction_frequency = StringField(' Interaction frequency :', [validators.Length(min=2, max=20)])
    grant_num = IntegerField('Grant Number :', [validators.Length(min=0, max=20)])

class ConferencesForm(Form):
    start_date = DateField('Start date :', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End date :', render_kw={"placeholder": "YYYY-MM-DD"})
    title = StringField('Title :', [validators.Length(min=3, max=20)])
    type = StringField(' Type :', [validators.Length(min=3, max=20)])
    role = StringField(' Role :', [validators.Length(min=2, max=20)])
    event_location = StringField('Event location :', [validators.Length(min=3, max=20)])
    grant_num = IntegerField('Grant Number :', [validators.Length(min=0, max=20)])

class CommunicationForm(Form):
    year = IntegerField('Year :', render_kw={"placeholder": "YYYY"})
    num_lectures = IntegerField('Number of Lectures :')
    num_visits = IntegerField('Number of Visits :')
    num_media_interactions = IntegerField('Number of Media Interactions :')

class FundingRatioForm(Form):
    year = IntegerField('Year :', render_kw={"placeholder": "YYYY"})
    percentage = IntegerField('Percentage :')

class EngagementsForm(Form):
    start_date = DateField('Start date :', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End date :', render_kw={"placeholder": "YYYY-MM-DD"})
    target_area = StringField('Target (Geographical) Area :', [validators.Length(min=3, max=40)])
    project_name = StringField('Project Name :', [validators.Length(min=3, max=40)])
    project_topic = StringField('Project Topic :', [validators.Length(min=3, max=40)])
    activity_type = StringField('Activity Type (Public-Event/In-Class/Other) :', [validators.Length(min=3, max=40)])