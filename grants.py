from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

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
    researcher_profile = db.relationship('Researcher_Profile', foreign_keys=research_Profile)


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









class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

"""
    ** Routes **
"""

@app.route("/")
@app.route("/index")
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("main_page.html", title="Home", comments=Comment.query.all())

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

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title='Profile', user=user)

@app.route('/user_edit/<username>', methods=['GET', 'POST'])
@login_required
def user_edit(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_edit.html', title='Edit Profile', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return render_template('edit_profile.html', title='Edit Profile')

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