from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps #ADDED for login
from flask_mail import Mail
#from email1 import send_password_reset_email
from time import time
import jwt
from forms import ResetPasswordRequestForm, ResetPasswordForm, DeletionForm, RegistrationForm, AddProposalForm, ProfileForm, EducationForm, GeneralForm
from wtforms.validators import ValidationError
from flask_dropzone import Dropzone
#from flask_wtf.csrf import CSRFProtect, CSRFError
import os
import requests
import xml.dom.minidom
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="cs3305team3",
    password="team3pass",
    hostname="cs3305team3.mysql.pythonanywhere-services.com",
    databasename="cs3305team3$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#csrf = CSRFProtect(app)
#@app.errorhandler(CSRFError)
#def csrf_error(e):
#    return e.description, 400
app.config.update(
                    DEBUG=True,
                    MAIL_SERVER='smtp.gmail.com',
                    MAIL_PORT=587,
                    MAIL_USE_TLS=1,
                    MAIL_USERNAME = 'sfigroup3@gmail.com',
                    MAIL_PASSWORD = 'sglarzpjdohssrpu',
                    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
                    DROPZONE_ALLOWED_FILE_CUSTOM = True,
                    DROPZONE_ALLOWED_FILE_TYPE = '.pdf, .txt',
                    #DROPZONE_ENABLE_CSRF = True,
                    DROPZONE_UPLOAD_ON_CLICK=True,

                    )

mail = Mail(app)

from email1 import send_password_reset_email
dropzone = Dropzone(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "ewlnzibewwlxshfkwmsi"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

"""
    ** Database Tables **
"""

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
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    f_name = db.Column(db.String(64))
    l_name = db.Column(db.String(64))
    job_title = db.Column(db.String(4))
    email = db.Column(db.String(80))
    ORCID = db.Column(db.Integer)
    login_id = db.Column(db.Integer)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Engagements(UserMixin, db.Model):

    __tablename__ = "engagements"

    engagement_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    f_name = db.Column(db.String(64))
    l_name = db.Column(db.String(64))
    job_title = db.Column(db.String(4))
    email = db.Column(db.String(80))
    ORCID = db.Column(db.Integer)
    login_id = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Presentations(UserMixin, db.Model):

    __tablename__ = "presentations"

    presentation_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    year = db.Column(db.Integer)
    type = db.Column(db.String(64))
    title = db.Column(db.String(20))
    organizing_body = db.Column(db.String(40))
    location = db.Column(db.String(40))
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class FundingRatio(UserMixin, db.Model):

    __tablename__ = "funding_ratio"

    funding_ratio_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    year = db.Column(db.Integer)
    percentage = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class TeamMembers(UserMixin, db.Model):

    __tablename__ = "team_members"

    team_member_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    departure_date = db.Column(db.DateTime)
    position = db.Column(db.String(64))
    name = db.Column(db.String(20))
    grant_number = db.Column(db.Integer)
    position = db.Column(db.String(30))
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Impacts(UserMixin, db.Model):

    __tablename__ = "impacts"

    impact_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    impact_title = db.Column(db.String(38))
    impact_category = db.Column(db.String(38))
    primary_beneficiary = db.Column(db.String(38))
    primary_attribution = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Funding_Diversification(UserMixin, db.Model):
    __tablename__ = "funding_diversifications"

    funding_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    funding_amount = db.Column(db.Integer)
    funding_body = db.Column(db.String(64))
    funding_programme = db.Column(db.String(64))
    status = db.Column(db.String(20))
    primary_attribution = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username



class EmploymentDB(UserMixin, db.Model):

    __tablename__ = "employment_db"

    employment_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    institution = db.Column(db.String(25))
    location = db.Column(db.String(21))
    year = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class AwardsDB(UserMixin, db.Model):

    __tablename__ = "awards_db"

    awards_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    awarding_body = db.Column(db.String(21))
    awarding_details = db.Column(db.String(100))
    member_name = db.Column(db.String(21))
    year = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Conferences(UserMixin, db.Model):
    __tablename__ = "conferences"

    conference_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    role = db.Column(db.String(64))
    event_location= db.Column(db.String(30))
    grant_num = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username



class Publications(UserMixin, db.Model):
    __tablename__ = "publications"

    publication_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    year = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    journal_conference_name = db.Column(db.String(64))
    published = db.Column(db.BOOLEAN)
    in_press = db.Column(db.BOOLEAN)
    doi = db.Column(db.Integer)
    grant_num = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Professional_Socities(UserMixin, db.Model):
    __tablename__ = "professional_socities"

    research_profile_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    name = db.Column(db.String(20))
    membership_type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username




class AcademicCollabs(UserMixin, db.Model):
    __tablename__ = "academic_collaborations"

    collaboration_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    department = db.Column(db.String(20))
    institution_name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    collaborator_name = db.Column(db.String(40))
    collaborator_goal = db.Column(db.String(40))
    interaction_frequency = db.Column(db.String(40))
    grant_number = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class NonAcademicCollabs(UserMixin, db.Model):
    __tablename__ = "non_academic_collaborations"

    non_academic_collaboration_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    department = db.Column(db.String(20))
    location = db.Column(db.String(64))
    collaborator_name = db.Column(db.String(40))
    collaborator_goal = db.Column(db.String(40))
    interaction_frequency = db.Column(db.String(40))
    grant_number = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Communication(UserMixin, db.Model):
    __tablename__ = "communication"

    research_profile_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    year = db.Column(db.Integer)
    num_lectures = db.Column(db.Integer)
    num_visits = db.Column(db.Integer)
    num_media_interactions= db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Innovations(UserMixin, db.Model):
    __tablename__ = "innovations"

    innovation_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    year = db.Column(db.Integer)
    type = db.Column(db.String(10))
    title = db.Column(db.String(25))
    grant_number = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


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
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    field_of_study = db.Column(db.String(35))
    degree = db.Column(db.String(20))
    institution = db.Column(db.String(20))
    year_of_degree = db.Column(db.Integer)
    research_Profile = db.Column(db.Integer, db.ForeignKey('researcher_profile.researcher_id'), nullable=True)
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username





class CFP(UserMixin, db.Model):

    __tablename__ = "call_for_proposals"
    call_id = db.Column(db.Integer, primary_key=True)
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






def login_required_advanced(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:#current_user.is_authenticated()
                return render_template("login_page.html", error=True)
            urole = current_user.get_user_type()
            if ( (urole != role) and (role != "ANY")):
                return render_template("login_page.html", error=True)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper







"""
                ********************
    ****************** Routes *********************
                ********************
"""

@app.route("/")
@app.route("/index")
def index():
    dom = xml.dom.minidom.parseString(requests.get('https://pub.sandbox.orcid.org/v3.0_rc1/0000-0002-9227-8514').text)
    eles = dom.documentElement
    zmin = eles.getElementsByTagName("personal-details:credit-name")[0].firstChild.data
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("main_page.html", title="Home", comments=Comment.query.all(), zmin=zmin)

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/login/", methods=["GET", "POST"])

def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    urole=user.get_user_type()
    login_user(user)
    #urole=user.get_user_type()
    if urole=="sfiAdmin":
        return redirect(url_for('admin_main'))

    elif urole=="researcher":
        return redirect(url_for('index'))

    elif urole=="researchCentre":
        return redirect(url_for('research_centre_main'))

    elif urole=="reviewer":
        return redirect(url_for('reviewer_main'))

    else:#user=institution:
        return redirect(url_for('institute_main'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password<token>', methods=['GET', 'POST'])#was /reset_password)reset_password<token>
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)

@app.route('/add_proposals', methods=["GET", "POST"])
@login_required_advanced(role="sfiAdmin")
def add_proposals():
    form = AddProposalForm(request.form)
    if request.method == 'POST' and form.validate():
        call=CFP(
            text_of_call=form.text_of_call.data,
            target_audience=form.target_audience.data,
            eligibility_criteria=form.eligibility_criteria.data,
            duration_of_award=form.duration_of_award.data,
            reporting_guidelines=form.reporting_guidelines.data,
            start_date=form.start_date.data,
            deadline=form.deadline.data
        )
        db.session.add(call)
        db.session.commit()
        return redirect(url_for('proposals'))
    return render_template('add_proposals.html', title='Proposals', user=user, form=form)

@app.route('/admin_main')
@login_required_advanced(role="sfiAdmin")
def admin_main():
    return render_template('admin_main_page.html', title='Proposals', user=current_user)#Delete user=user

@app.route('/research_centre_main')
@login_required_advanced(role="researchCentre")
def research_centre_main():
    return render_template('research_centre_main_page.html', title='Research Centre', user=current_user)

@app.route('/reviewer_main')
@login_required_advanced(role="reviewer")
def reviewer_main():
    return render_template('reviewer_main.html', title='Reviewer', user=current_user)

@app.route('/institute_main')
@login_required_advanced(role="institution")
def institute_main():
    return render_template('institute_main.html', title='Insititution', user=current_user)

@app.route('/proposals')
def proposals():
    calls=CFP.query.all()
    return render_template('call_for_proposals.html', title='Proposals', user=user, calls=calls)

def getPasswordHash(password):
    return generate_password_hash(password)

@app.route('/delete_user', methods=['GET', 'POST'])
@login_required_advanced(role="sfiAdmin")
def delete_user():
    form = DeletionForm(request.form)
    users=User.query.all()
    if request.method == 'POST' and form.validate():
        User.query.filter(User.id == form.user_id.data).delete()
        db.session.commit()
        return redirect(url_for('delete_user'))
    return render_template('delete_user.html', title='Delete User', users=users, form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
            if key.startswith('file'):
                #save_as = f.filename + current_user.get_id()
                #directory = current_user.get_id()
                f.save(os.path.join(app.config['UPLOADED_PATH'], str(current_user.get_id())))
    return render_template('drag_and_drop.html', title='Proposals', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data, user_type=form.user_type.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/submit_proposals')
#@login_required_advanced(role="sfiAdmin")
def submit_proposals():
    return render_template('submit_proposals.html', title='Proposals', user=user)

@app.route('/user/<username>', methods=['GET', 'POST'])
#@login_required
#@login_required_advanced(role="researcher")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        researcher = Researcher_Profile(ORCID=form.orcid.data)

    return render_template('user.html', title='Profile', user=user, form=form)

@app.route('/user/education_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def education_form():
    form = EducationForm(request.form)
    if request.method == 'POST' and form.validate():
        makeAssignment="makeAssignmentHere"
    return render_template('forms/education_form.html', title='Education', user=user, form=form)

@app.route('/user/general_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def general_form():
    form = GeneralForm(request.form)
    if request.method == 'POST' and form.validate():
        anotherEmptyAssignment="anotherEmptyAssignmentHere"
    return render_template('forms/general_form.html', title='Education', user=user, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    return render_template('edit_profile.html', title='Edit Profile')

@app.route('/user_edit/<username>', methods=['GET', 'POST'])
@login_required_advanced(role="researcher")
def user_edit(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_edit.html', title='Edit Profile', user=user)


@app.route("/home")
def home():
    return render_template('home.html', title='Profile')

"""
    ** Redundant Class **
"""

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)