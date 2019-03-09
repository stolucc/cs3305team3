from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from time import time
from grants import db
import jwt
from wtforms.validators import ValidationError

class SFIAdmin(UserMixin, db.Model):

    __tablename__ = "sfiAdmin"

    sfi_admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    loginID = db.Column(db.Integer, db.ForeignKey('login_account.login_account_id'), nullable=True)
    loginDetails = db.relationship('Login_Account', foreign_keys=loginID)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Reviewer(UserMixin, db.Model):

    __tablename__ = "reviewer"

    reviewer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80))
    loginID = db.Column(db.Integer, db.ForeignKey('login_account.login_account_id'), nullable=True)
    loginDetails = db.relationship('Login_Account', foreign_keys=loginID)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Researcher_Account(UserMixin, db.Model):

    __tablename__ = "researcher_account"

    researcher_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Research_Centre_Admin(UserMixin, db.Model):

    __tablename__ = "research_centre_admin"

    research_centre_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    research_profile = db.Column(db.Integer)
    online = db.Column(db.BOOLEAN)
    loginID = db.Column(db.Integer, db.ForeignKey('login_account.login_account_id'), nullable=True)
    loginDetails = db.relationship('Login_Account', foreign_keys=loginID)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Login_Account(UserMixin, db.Model):

    __tablename__ = "login_account"

    login_account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Researcher_Profile(UserMixin, db.Model):

    __tablename__ = "researcher_profile"

    researcher_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(64))
    l_name = db.Column(db.String(64))
    job_title = db.Column(db.String(40))
    ORCID = db.Column(db.String(19))
    prefix = db.Column(db.String(10))
    suffix = db.Column(db.String(10))
    phone = db.Column(db.Integer)
    phone_extension = db.Column(db.Integer)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Engagements(UserMixin, db.Model):

    __tablename__ = "engagements"

    engagement_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    activity_type = db.Column(db.String(30))
    project_topic = db.Column(db.String(45))
    target_area = db.Column(db.String(80))

    grant_application = db.Column(db.Integer, db.ForeignKey('grant_application.grant_application_id'), nullable=True)
    grant_applications = db.relationship('Grant_Application', foreign_keys=grant_application)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Presentations(UserMixin, db.Model):

    __tablename__ = "presentations"

    presentation_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    type = db.Column(db.String(64))
    title = db.Column(db.String(20))
    organizing_body = db.Column(db.String(40))
    location = db.Column(db.String(40))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class FundingRatio(UserMixin, db.Model):

    __tablename__ = "funding_ratio"

    funding_ratio_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    percentage = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class TeamMembers(UserMixin, db.Model):

    __tablename__ = "team_members"

    team_member_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    departure_date = db.Column(db.DateTime)
    name = db.Column(db.String(20))
    position = db.Column(db.String(30))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Impacts(UserMixin, db.Model):

    __tablename__ = "impacts"

    impact_id = db.Column(db.Integer, primary_key=True)
    impact_title = db.Column(db.String(38))
    impact_category = db.Column(db.String(38))
    primary_beneficiary = db.Column(db.String(38))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Funding_Diversification(UserMixin, db.Model):

    __tablename__ = "funding_diversifications"

    funding_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    funding_amount = db.Column(db.Integer)
    funding_body = db.Column(db.String(64))
    funding_programme = db.Column(db.String(64))
    status = db.Column(db.String(20))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username



class Grant_Application(UserMixin, db.Model):

    __tablename__ = "grant_application"

    grant_application_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    proposal_title = db.Column(db.String(30))
    award_duration = db.Column(db.String(30))
    national_research_priority = db.Column(db.String(60))
    sfi_legal_remit_justification = db.Column(db.String(2000))
    ethical_issues = db.Column(db.String(200))
    applicants_country = db.Column(db.String(40))
    scientific_abstract = db.Column(db.String(2000))
    lay_abstract = db.Column(db.String(1000))
    programme_documents = db.Column(db.String(1000))
    approved = db.Column(db.Boolean, default=False)
    reviewer_approved = db.Column(db.Boolean, default=False)


    def set_propsoal_title(self, title):
        self.proposal_title  = title

    def set_award_duration(self, duration):
        self.award_duration = duration

    def set_national_research_priority(self, priority):
        self.national_research_priority = priority

    def set_sfi_legal_remit_justification(self, justification):
        self.sfi_legal_remit_justification= justification

    def set_ethical_issues(self, issue):
        self.ethical_issues = issue

    def set_applicants_country(self, country):
        self.applicants_country = country

    def set_scientific_abstract(self, abstract):
        self.scientific_abstract = abstract

    def set_lay_abstract(self, abstract):
        self.lay_abstract = abstract

    def set_programme_documents(self, documents):
        self.programme_documents = documents

class Co_Applicants(UserMixin, db.Model):
    __tablename__="coapplicants_db"
    coapplicant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    organization = db.Column(db.String(80))
    email = db.Column(db.String(80))
    grant_application = db.Column(db.Integer, db.ForeignKey('grant_application.grant_application_id'), nullable=True)
    grant_applications = db.relationship('Grant_Application', foreign_keys=grant_application)

class Collaborators(UserMixin, db.Model):
    __tablename__="collaborators_db"
    collaborator_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    organization = db.Column(db.String(80))
    email = db.Column(db.String(80))
    grant_application = db.Column(db.Integer, db.ForeignKey('grant_application.grant_application_id'), nullable=True)
    grant_applications = db.relationship('Grant_Application', foreign_keys=grant_application)


class EmploymentDB(UserMixin, db.Model):

    __tablename__ = "employment_db"

    employment_id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(25))
    location = db.Column(db.String(21))
    year = db.Column(db.Integer)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class AwardsDB(UserMixin, db.Model):

    __tablename__ = "awards_db"

    awards_id = db.Column(db.Integer, primary_key=True)
    awarding_body = db.Column(db.String(21))
    awarding_details = db.Column(db.String(100))
    member_name = db.Column(db.String(21))
    year = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Conferences(UserMixin, db.Model):
    __tablename__ = "conferences"

    conference_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    role = db.Column(db.String(64))
    event_location= db.Column(db.String(30))
    grant_num = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username



class Publications(UserMixin, db.Model):
    __tablename__ = "publications"

    publication_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    journal_conference_name = db.Column(db.String(64))
    published = db.Column(db.BOOLEAN)
    in_press = db.Column(db.BOOLEAN)
    doi = db.Column(db.Integer)

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Professional_Societies(UserMixin, db.Model):
    __tablename__ = "professional_societies"

    research_profile_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    name = db.Column(db.String(20))
    membership_type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username



class AcademicCollabs(UserMixin, db.Model):
    __tablename__ = "academic_collaborations"

    collaboration_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    department = db.Column(db.String(20))
    institution_name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    collaborator_name = db.Column(db.String(40))
    collaborator_goal = db.Column(db.String(40))
    interaction_frequency = db.Column(db.String(40))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class NonAcademicCollabs(UserMixin, db.Model):
    __tablename__ = "non_academic_collaborations"

    non_academic_collaboration_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    department = db.Column(db.String(20))
    institution_name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    collaborator_name = db.Column(db.String(40))
    collaborator_goal = db.Column(db.String(40))
    interaction_frequency = db.Column(db.String(40))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Communication(UserMixin, db.Model):
    __tablename__ = "communication"

    research_profile_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    num_lectures = db.Column(db.Integer)
    num_visits = db.Column(db.Integer)
    num_media_interactions= db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class SubmittedApplications(UserMixin, db.Model):
    __tablename__ = "submitted_applications"
    grant_application_id = db.Column(db.Integer, primary_key=True)
    proposal_name = db.Column(db.String(128))



class Innovations(UserMixin, db.Model):
    __tablename__ = "innovations"

    innovation_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    type = db.Column(db.String(10))
    title = db.Column(db.String(25))

    grant_reference = db.Column(db.Integer, db.ForeignKey('submitted_applications.grant_application_id'))
    grant_reference_id = db.relationship('SubmittedApplications', foreign_keys=grant_reference)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class AnnualReports(UserMixin, db.Model):
    __tablename__ = "annual_reports"

    annual_report_id = db.Column(db.Integer, primary_key=True)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    publication_id = db.Column(db.Integer, db.ForeignKey('publications.publication_id'), nullable=True)
    publication = db.relationship('Publications', foreign_keys=publication_id)

    academic_collab_id = db.Column(db.Integer, db.ForeignKey('academic_collaborations.collaboration_id'), nullable=True)
    collaborations = db.relationship('AcademicCollabs', foreign_keys=academic_collab_id)

    education_id = db.Column(db.Integer, db.ForeignKey('researcher_education.researcher_education_id'), nullable=True)
    researcher_education = db.relationship('ResearcherEducation', foreign_keys=education_id)

    non_academic_collab_id = db.Column(db.Integer, db.ForeignKey('non_academic_collaborations.non_academic_collaboration_id'), nullable=True)
    non_academic_collabs = db.relationship('NonAcademicCollabs', foreign_keys=non_academic_collab_id)

    impact_id = db.Column(db.Integer, db.ForeignKey('impacts.impact_id'), nullable=True)
    impacts = db.relationship('Impacts', foreign_keys=impact_id)

    innovations_id = db.Column(db.Integer, db.ForeignKey('innovations.innovation_id'), nullable=True)
    innovations = db.relationship('Innovations', foreign_keys=innovations_id)

class ResearcherEducation(UserMixin, db.Model):
    __tablename__ = "researcher_education"

    researcher_education_id = db.Column(db.Integer, primary_key=True)
    field_of_study = db.Column(db.String(35))
    degree = db.Column(db.String(20))
    institution = db.Column(db.String(20))
    location = db.Column(db.String(45))
    year_of_degree = db.Column(db.Integer)

    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    UserDetails = db.relationship('User', foreign_keys=users)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class CFP(UserMixin, db.Model):

    __tablename__ = "call_for_proposals"
    call_id = db.Column(db.Integer, primary_key=True)
    call_for_proposal_title= db.Column(db.String(20))
    deadline= db.Column(db.DateTime)
    text_of_call= db.Column(db.String(300))
    target_audience= db.Column(db.String(80))
    eligibility_criteria= db.Column(db.String(70))
    duration_of_award= db.Column(db.String(70))
    reporting_guidelines= db.Column(db.String(50))
    start_date= db.Column(db.DateTime)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, index=True)
    user_type = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

    def get_user_type(self):
        return self.user_type

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
