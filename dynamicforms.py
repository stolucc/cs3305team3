from flask_wtf import FlaskForm
from wtforms import  BooleanField, SelectField, StringField, HiddenField, PasswordField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


def max_words_200(form, field):
    #Function to test if there are more words in a field than are allowed
    max_words = 200
    if len(field.data.split()) > max_words:
        error_message = "Must be less than" + str(max_words) + "words"
        raise ValidationError(error_message)

def max_words_100(form, field):
    #Function to test if there are more words in a field than are allowed
    max_words = 100
    if len(field.data.split()) > max_words:
        error_message = "Must be less than" + str(max_words) + "words"
        raise ValidationError(error_message)

def max_words_250(form, field):
    #Function to test if there are more words in a field than are allowed
    max_words = 250
    if len(field.data.split()) > max_words:
        error_message = "Must be less than" + str(max_words) + "words"
        raise ValidationError(error_message)


class GrantGeneralInfoForm(FlaskForm):
    grant_application_id = HiddenField( render_kw={"readonly": True})
    proposal_title = StringField('Proposal Title', [validators.Length(min=1, max=800, message="Must be less than 100 characters")], render_kw={"readonly": True})
    #award_duration = SelectField('Award Duration', choices=[("Priority Area A - Future Networks & Communications"),("Priority Area B - Data Analytics, Management, Security & Privacy")],render_kw={"placeholder": "Duration of requested award in months"})
    award_duration = StringField('Award Duration', [validators.Length(min=6, max=900, message="Field must be less than 100 characters")], render_kw={"placeholder":"In months"})
    national_research_priority  = SelectField(u'National Research Priority', choices=[
        ('Priority Area A - Future Networks & Communications', 'Priority Area A - Future Networks & Communications'),
        ('Priority Area B - Data Analytics, Management, Security & Privacy', 'Priority Area B - Data Analytics, Management, Security & Privacy'),
        ('Priority Area C - Digital Platforms, Content & Applications', 'Priority Area C - Digital Platforms, Content & Applications'),
        ('Priority Area D - Connected Health and Independent Living', 'Priority Area D - Connected Health and Independent Living'),
        ('Priority Area E - Medical Devices', 'Priority Area E - Medical Devices'),
        ('Priority Area F - Diagnostics', 'Priority Area F - Diagnostics'),
        ('Priority Area G - Therapeutics; Synthesis, Formulation, Processing and Drug Delivery', 'Priority Area G - Therapeutics; Synthesis, Formulation, Processing and Drug Delivery'),
        ('Priority Area H - Food For Health', 'Priority Area H - Food For Health'),
        ('Priority Area I - Sustainable Food Production and Processing', 'Priority Area I - Sustainable Food Production and Processing'),
        ('Priority Area J - Marine Renewable Energ', 'Priority Area J - Marine Renewable Energy'),
        ('Priority Area K - Smart Grids & Smart Cities', 'Priority Area K - Smart Grids & Smart Cities'),
        ('Priority Area L - Manufacturing Competitiveneess', 'Priority Area L - Manufacturing Competitiveneess'),
        ('Priority Area M - Processing Technologies and Novel Materials', 'Priority Area M - Processing Technologies and Novel Materials'),
        ('Priority Area N - Innovation in Services and Business Processes', 'Priority Area N - Innovation in Services and Business Processes'),
        ('Software', 'Software'),
        ('Other', 'Other')])
    #StringField('National Research Priority', [validators.Length(min=6, max=30)], render_kw={"placeholder": "Proven track record with funding"})
    sfi_legal_remit_justification = TextAreaField("Please Describe how your proposal is aligned with SFI's legal remit", [validators.Length(min=6, max=500, message="Please provide less than 250 words")], render_kw={"placeholder": "Please provide less than 250 words"})
    ethical_issues = StringField('Ethical Issues', [max_words_250], render_kw={"placeholder":" -A statement indicating whether the research involves the use of animals"})
    applicants_country = StringField('Applicants Country', [validators.Length(min=6, max=800)], render_kw={"placeholder":"Applicants country at time of submission"})

class GrantScientificAbstractForm(FlaskForm):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=900, message="Application ID should be no longer than 20 spaces")],render_kw={"readonly": True})
    scientific_abstract =  TextAreaField('Scientific Abstract', [max_words_200], render_kw={"placeholder": "Please don't submit more than 200 words"})

class GrantLayAbstractForm(FlaskForm):
    grant_application_id = HiddenField('Grant Application ID',  [validators.Length(min=1, max=900, message="Application ID should be no longer than 20 spaces")],render_kw={"readonly": True})
    lay_abstract = TextAreaField('Lay Abstract', [max_words_100], render_kw={"placeholder": "Please don't submit more than 100 words"})

class CoApplicantsForm(FlaskForm):
    coapplicant_id = HiddenField('Co Applicant ID',  [validators.Length( max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})
    #name = StringField('Name',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})

    name = StringField('Name:', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Please enter the name of the co-applicant"})
    organization = StringField('Organization:', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Please enter the Organization of the co-applicant"})
    email = StringField('Email:', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Please enter the email of the co-applicant"})
    grant_application = HiddenField('Grant Application',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})


class CollaboratorsForm(FlaskForm):
    collaborators_id = HiddenField('Collabarators ID',  [validators.Length( max=500, message="CollabaratorField be 10 digits (no spaces)")],render_kw={"readonly": True})
    #name = StringField('Name',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})

    name = StringField('Name:', [validators.Length(min=1, max=300)], render_kw={"placeholder": "Please enter the name of the collaborator"})
    organization = StringField('Organization:', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Please enter the Organization of the Collaborator"})
    email = StringField('Email:', [validators.Length(min=6, max=45)], render_kw={"placeholder": "Please enter the email of the Collaborator"})
    grant_application = HiddenField('Grant Application',  [validators.Length(min=1, max=500, message="Application Field be 10 digits (no spaces)")],render_kw={"readonly": True})


